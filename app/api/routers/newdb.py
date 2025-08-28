from fastapi import APIRouter, HTTPException
from app.db.mysql import get_secondary_db

router = APIRouter(prefix="/newdb", tags=["newdb"])


@router.post("/products")
def create_product(product: dict):
    with get_secondary_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO products (name, description, price, category) VALUES (%s, %s, %s, %s)",
                (
                    product.get("name"),
                    product.get("description"),
                    product.get("price"),
                    product.get("category"),
                ),
            )
            conn.commit()
            product_id = cursor.lastrowid
            return {**product, "id": product_id, "created_at": "刚刚"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/products")
def get_products():
    with get_secondary_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, description, price, category, created_at FROM products ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        for row in rows:
            if row["created_at"]:
                row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        return rows


@router.post("/orders")
def create_order(order: dict):
    with get_secondary_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO orders (customer_name, product_id, quantity, total_amount) VALUES (%s, %s, %s, %s)",
                (
                    order.get("customer_name"),
                    order.get("product_id"),
                    order.get("quantity"),
                    order.get("total_amount"),
                ),
            )
            conn.commit()
            order_id = cursor.lastrowid
            return {**order, "id": order_id, "order_date": "刚刚"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders")
def get_orders():
    with get_secondary_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT o.id, o.customer_name, o.product_id, o.quantity, o.total_amount, o.order_date,
                   p.name as product_name
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.id
            ORDER BY o.order_date DESC
            """
        )
        rows = cursor.fetchall()
        for row in rows:
            if row["order_date"]:
                row["order_date"] = row["order_date"].strftime("%Y-%m-%d %H:%M:%S")
        return rows


