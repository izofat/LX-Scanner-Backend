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
        )
        self.conn = None

    def get_connection(self):
        if self.conn is None or not self.conn.is_connected():
            self.conn = self.connection.get_connection()
        return self.conn

    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
