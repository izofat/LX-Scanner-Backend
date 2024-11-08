import mysql.connector

from settings import MySqlConfig


class DbConnection:
    def __init__(self, config=MySqlConfig):
        self.connection = mysql.connector.pooling.MySQLConnectionPool(
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE,
            pool_name=config.POOL_NAME,
            pool_size=config.POOL_SIZE,
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
        )
        self.conn = None

    def __enter__(self):
        self.conn = self.connection.get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if self.conn.is_connected():
                self.conn.close()  # This returns the connection to the pool
            self.conn = None
