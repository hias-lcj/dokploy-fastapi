from fastapi import APIRouter, Depends, HTTPException
from mysql.connector import MySQLConnection
from database_rds import get_rds_connection

router = APIRouter(prefix="/rds", tags=["RDS 只读数据库"])


@router.get("/users")
def get_users_from_rds(db: MySQLConnection = Depends(get_rds_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, content, message_time FROM chat_message LIMIT 10")
        users = cursor.fetchall()
        return {"data": users, "total": len(users), "source": "阿里云 RDS"}
    except Exception as e:
        print(f"RDS查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"RDS查询失败: {str(e)}")
    finally:
        cursor.close()


