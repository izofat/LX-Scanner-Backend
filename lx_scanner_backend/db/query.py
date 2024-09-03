from .connection import DbConnection


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._create_account_table()
        self._create_scanner_input_table()
        self._create_scanner_output_table()

    def execute_query(self, query: str, is_insert: bool = False, *args):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, (*args,))
            if is_insert:
                conn.commit()
                return cursor.rowcount

            result = cursor.fetchall()
            return result

        except Exception as e:
            raise e

    def _create_account_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS account (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(300) NOT NULL UNIQUE,
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

    @property
    def register_account(self):
        query = f"""
            INSERT IGNORE INTO account (username, password)
            VALUES (%s, %s)
        """
        return query
