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

    def get_connection(self):
        return self.connection.get_connection()
