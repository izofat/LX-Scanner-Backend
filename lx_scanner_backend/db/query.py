from .connection import DbConnection


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._create_account_table()
        self._create_scanner_input_table()
        self._create_scanner_output_table()

    def execute_query(self, query: str, *args, is_commit: bool = False):
        conn = self.connection.get_connection()
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
            expectedOutput VARCHAR(300) NOT NULL,
            fileName VARCHAR(300) NOT NULL,
            inputLanguage VARCHAR(30) DEFAULT 'en',
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

    def register_account(self, username: str, password: str):
        query = """
            INSERT IGNORE INTO account (username, password)
            VALUES (%s, %s)
        """
        return self.execute_query(query, username, password, is_commit=True)

    def get_user(self, username: str):
        query = """
            SELECT username, password FROM account WHERE username = %s 
        """
        return self.execute_query(query, username)

    def get_user_id(self, username: str):
        query = """
            SELECT id FROM account WHERE username = %s AND password = %s
        """
        return self.execute_query(query, username)

    def insert_scanner_input(
        self, user_id: int, expected_output: str, file_Name: str, input_language: str
    ):
        query = """
            INSERT INTO scannerInput (userId, expectedOutput, fileName, inputLanguage)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(
            query, user_id, expected_output, file_Name, input_language, is_commit=True
        )
