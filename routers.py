# routers.py
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import UserCreate, UserResponse
import mysql.connector

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (user.name, user.email)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return {**user.dict(), "id": user_id, "created_at": "刚刚"}
        except mysql.connector.IntegrityError:
            raise HTTPException(status_code=400, detail="邮箱已存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def get_users():
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")

        rows = cursor.fetchall()
        # 格式化时间
        for row in rows:
            row['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return rows