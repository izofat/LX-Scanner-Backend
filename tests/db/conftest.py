import mysql.connector
import pytest

from settings import MySqlConfig


def create_connection():
    connection = mysql.connector.connect(
        host=MySqlConfig.HOST,
        port=MySqlConfig.PORT,
        user=MySqlConfig.USER,
        password=MySqlConfig.PASSWORD,
        database=MySqlConfig.DATABASE,
    )

    return connection


@pytest.fixture(scope="module")
def db_connection():
    connection = create_connection()
    yield connection
    connection.close()
