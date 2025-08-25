# routers_rds.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from database_rds import get_rds_connection


router = APIRouter(prefix="/rds", tags=["RDS 只读数据库"])

@router.get("/users")
def get_users_from_rds(db: MySQLConnection = Depends(get_rds_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        # ✅ 替换为你的实际表名
        cursor.execute("SELECT id, content, message_time FROM chat_message LIMIT 10")
        users = cursor.fetchall()
        return {"data": users, "total": len(users), "source": "阿里云 RDS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
    finally:
        cursor.close()