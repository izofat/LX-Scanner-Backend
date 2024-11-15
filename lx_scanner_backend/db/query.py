from datetime import datetime
from typing import Optional

from .connection import DbConnection


class BaseQuery:  # pylint: disable=too-few-public-methods
    def __init__(self, connection):
        self._connection = connection

    def execute_query(self, query: str, *args, is_commit: bool = False):
        with self._connection as conn:
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(query, (*args,))
                if is_commit:
                    conn.commit()
                    return cursor.rowcount

                result = cursor.fetchall()
                return result

            except Exception as e:
                raise e
            finally:
                cursor.close()


class TableQueries(BaseQuery):
    def create_account_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS account (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(300) NOT NULL
            )
        """
        return self.execute_query(query)

    def create_scanner_input_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS scannerInput (
                id INT AUTO_INCREMENT PRIMARY KEY,
                userId INT,
                name VARCHAR(200),
                expectedOutput VARCHAR(300),
                status ENUM('pending', 'processing', 'completed', 'failed')
                DEFAULT 'pending' NOT NULL,
                inputLanguage VARCHAR(30) DEFAULT 'en',
                fileName VARCHAR(300) NOT NULL,
                FOREIGN KEY (userId) REFERENCES lxScanner.account(id)
            )
        """
        return self.execute_query(query)

    def create_scanner_output_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS scannerOutput (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scannerInputId INT NOT NULL,
                userId INT NOT NULL,
                outputText VARCHAR(300),
                confidence DECIMAL(5, 2),
                fileName VARCHAR(100),
                FOREIGN KEY (scannerInputId) REFERENCES scannerInput(id),
                FOREIGN KEY (userId) REFERENCES account(id)
            )
        """
        return self.execute_query(query)

    def create_token_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS token (
                id INT AUTO_INCREMENT PRIMARY KEY,  
                userId INT NOT NULL,
                jwtToken VARCHAR(2000) NOT NULL,
                jwtExpireDate DATETIME NOT NULL,
                FOREIGN KEY (userId) REFERENCES account(id)
            )
        """
        return self.execute_query(query)


class SelectQueries(BaseQuery):
    def get_user(self, username: str):
        query = """
            SELECT id, username, password FROM account WHERE username = %s 
        """
        return self.execute_query(query, username)

    def get_token(self, user_id: int):
        query = """
            SELECT id, userId, jwtToken, jwtExpireDate FROM token 
            WHERE userId = %s
            ORDER BY jwtExpireDate DESC
            LIMIT 1
        """
        return self.execute_query(query, user_id)

    def get_all_images(self, user_id: int):
        query = """
            SELECT id, status, expectedOutput, fileName, inputLanguage 
            FROM scannerInput WHERE userId = %s
        """
        return self.execute_query(query, user_id)

    def get_image_by_id(self, image_id: int):
        query = """
            SELECT id, status, expectedOutput, fileName, inputLanguage 
            FROM scannerInput WHERE id = %s
        """
        return self.execute_query(query, image_id)

    def get_image_by_name(self, name: str):
        query = """
            SELECT id, status, expectedOutput, fileName, inputLanguage 
            FROM scannerInput WHERE name = %s
        """
        return self.execute_query(query, name)


class InsertQueries(BaseQuery):
    def register_account(self, username: str, password: str):
        query = """
            INSERT IGNORE INTO account (username, password)
            VALUES (%s, %s)
        """
        return self.execute_query(query, username, password, is_commit=True)

    def insert_scanner_input(
        self,
        user_id: int,
        name: Optional[str],
        expected_output: Optional[str],
        file_name: str,
        input_language: str,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        query = """
            INSERT INTO scannerInput (userId, name, expectedOutput, fileName, inputLanguage)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query,
            user_id,
            name,
            expected_output,
            file_name,
            input_language,
            is_commit=True,
        )

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        query = """
            INSERT INTO token (userId, jwtToken, jwtExpireDate)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(
            query, user_id, jwt_token, jwt_expire_date, is_commit=True
        )


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._tables = TableQueries(self.connection)
        self._select = SelectQueries(self.connection)
        self._insert = InsertQueries(self.connection)

        # Create tables
        self._tables.create_account_table()
        self._tables.create_scanner_input_table()
        self._tables.create_scanner_output_table()
        self._tables.create_token_table()

    # Select methods
    def get_user(self, username: str):
        return self._select.get_user(username)

    def get_token(self, user_id: int):
        return self._select.get_token(user_id)

    def get_all_images(self, user_id: int):
        return self._select.get_all_images(user_id)

    def get_image_by_id(self, image_id: int):
        return self._select.get_image_by_id(image_id)

    def get_image_by_name(self, image_name: str):
        return self._select.get_image_by_name(image_name)

    # Insert methods
    def register_account(self, username: str, password: str):
        return self._insert.register_account(username, password)

    def insert_scanner_input(
        self,
        user_id: int,
        name: Optional[str],
        expected_output: Optional[str],
        file_name: str,
        input_language: str,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        return self._insert.insert_scanner_input(
            user_id, name, expected_output, file_name, input_language
        )

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        return self._insert.insert_token(user_id, jwt_token, jwt_expire_date)
