import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from app.core.config import settings


def _make_config(host: str, user: str, password: str, database: str, port: int):
    return {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
        "port": port,
        'ssl_disabled': True,
    }


primary_config = _make_config(
    settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_DATABASE, settings.DB_PORT
)

secondary_config = _make_config(
    settings.NEW_DB_HOST, settings.NEW_DB_USER, settings.NEW_DB_PASSWORD, settings.NEW_DB_DATABASE, settings.NEW_DB_PORT
)


@contextmanager
def get_primary_db():
    connection = None
    try:
        connection = mysql.connector.connect(**primary_config)
        if connection.is_connected():
            yield connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


@contextmanager
def get_secondary_db():
    connection = None
    try:
        connection = mysql.connector.connect(**secondary_config)
        if connection.is_connected():
            yield connection
    except Error as e:
        print(f"新数据库连接错误: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


