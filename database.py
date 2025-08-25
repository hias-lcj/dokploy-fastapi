# database.py
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env
# 数据库连接配置
config = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    # 'host': '111.231.24.125',
    # 'user': 'mysqldb',
    # 'password': 'mpxhsr29ltu63a9c',
    # 'database': 'mysqldb',
    'port': 3306,
    'ssl_disabled': True,
}

@contextmanager
def get_db():
    """提供数据库连接的上下文管理器"""
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            yield connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()