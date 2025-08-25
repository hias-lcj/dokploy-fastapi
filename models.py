# models.py
from database import get_db

def create_users_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("✅ users 表已准备就绪")
        