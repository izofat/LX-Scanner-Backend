import pytest
from mysql.connector.connection import MySQLConnectionAbstract
from mysql.connector.errors import Error


def test_connection(db_connection: MySQLConnectionAbstract):
    try:
        assert db_connection.is_connected(), "Connection to the database failed"
    except Error as e:
        pytest.fail(f"Failed to connect to the database: {e}")
