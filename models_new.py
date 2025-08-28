# models_new.py
from app.db.mysql import get_secondary_db

def create_products_table():
    """创建产品表"""
    query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """
    with get_secondary_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("✅ products 表已准备就绪")

def create_orders_table():
    """创建订单表"""
    query = """
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        product_id INT,
        quantity INT NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    ) ENGINE=InnoDB;
    """
    with get_secondary_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("✅ orders 表已准备就绪")
