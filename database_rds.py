# database_rds.py
import mysql.connector
from mysql.connector import Error
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env

# 只读数据库配置（阿里云 RDS）
RDS_CONFIG = {
    "host": os.getenv("RDS_HOST"),
    "user": os.getenv("RDS_USER"),
    "password": os.getenv("RDS_PASSWORD"),
    "database": os.getenv("RDS_DATABASE"),
    "port": 3306,
    "autocommit": True,
    "connection_timeout": 10,
}

def get_rds_connection():
    """获取 RDS 只读连接"""
    try:
        conn = mysql.connector.connect(**RDS_CONFIG)
        if conn.is_connected():
            return conn
        else:
            raise HTTPException(status_code=500, detail="无法连接到 RDS 数据库")
    except Error as e:
        print(f"RDS 连接错误: {e}")
        raise HTTPException(status_code=500, detail=f"数据库连接失败: {str(e)}")