from fastapi import APIRouter, HTTPException
from app.db.mysql import get_primary_db
from mysql import connector as mysql

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: dict):
    with get_primary_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (user.get("name"), user.get("email")),
            )
            conn.commit()
            user_id = cursor.lastrowid
            return {**user, "id": user_id, "created_at": "刚刚"}
        except mysql.IntegrityError:
            raise HTTPException(status_code=400, detail="邮箱已存在")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_users():
    with get_primary_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        for row in rows:
            row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        return rows


