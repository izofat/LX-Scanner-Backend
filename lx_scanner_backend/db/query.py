from datetime import datetime
from typing import Optional

from .connection import DbConnection


class TableQueries:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.connection = DbConnection()
        self._create_account_table()
        self._create_scanner_input_table()
        self._create_scanner_output_table()
        self._create_token_table()

    def execute_query(self, query: str, *args, is_commit: bool = False):
        with self.connection as conn:
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

    def _create_account_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS account (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(300) NOT NULL
            )
        """
        self.execute_query(query)

    def _create_scanner_input_table(self):
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
        self.execute_query(query)

    def _create_scanner_output_table(self):
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
        self.execute_query(query)

    def _create_token_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS token (
                id INT AUTO_INCREMENT PRIMARY KEY,  
                userId INT NOT NULL,
                jwtToken VARCHAR(2000) NOT NULL,
                jwtExpireDate DATETIME NOT NULL,
                FOREIGN KEY (userId) REFERENCES account(id)
            )
        """
        self.execute_query(query)


class Query(TableQueries):
    def register_account(self, username: str, password: str):
        query = """
            INSERT IGNORE INTO account (username, password)
            VALUES (%s, %s)
        """
        return self.execute_query(query, username, password, is_commit=True)

    def get_user(self, username: str):
        query = """
            SELECT id, username, password FROM account WHERE username = %s 
        """
        return self.execute_query(query, username)

    def insert_scanner_input(
        self,
        user_id: int,
        expected_output: Optional[str],
        file_name: str,
        input_language: str,
    ):
        query = """
            INSERT INTO scannerInput (userId, name, expectedOutput, fileName, inputLanguage)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query, user_id, expected_output, file_name, input_language, is_commit=True
        )

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        query = """
            INSERT INTO token (userId, jwtToken, jwtExpireDate)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(
            query, user_id, jwt_token, jwt_expire_date, is_commit=True
        )

    def get_token(self, user_id: int):
        query = """
            SELECT id, userId, jwtToken, jwtExpireDate FROM token 
            WHERE userId = %s
            ORDER BY jwtExpireDate DESC
            LIMIT 1
        """
        return self.execute_query(query, user_id)
