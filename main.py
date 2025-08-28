# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routers.users import router as users_router
from app.api.routers.rds import router as rds_router
from app.api.routers.newdb import router as newdb_router
from app.api.routers.llm import router as llm_router
from models import create_users_table
from models_new import create_products_table, create_orders_table
import uvicorn
import webbrowser
import threading

app = FastAPI(title="FastAPI 多数据库 + LLM 系统", version="2.1")

@app.on_event("startup")
def startup_event():
    create_users_table()
    try:
        create_products_table()
        create_orders_table()
        print("✅ 新数据库表已准备就绪")
    except Exception as e:
        print(f"⚠️ 新数据库表创建失败: {e}")

    threading.Thread(target=lambda: webbrowser.open("http://localhost:8000/static/index.html")).start()


app.include_router(users_router)
app.include_router(rds_router)
app.include_router(newdb_router)
app.include_router(llm_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {
        "message": "多数据库 + LLM FastAPI 服务",
        "docs": "/docs",
        "local_users": "/users",
        "rds_users": "/rds/users",
        "newdb_products": "/newdb/products",
        "newdb_orders": "/newdb/orders",
        "llm_chat": "/llm/chat",
        "frontend": "/static/index.html",
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
#     地址	用途
# http://localhost:8000	查看 API 信息
# http://localhost:8000/docs	Swagger 文档
# http://localhost:8000/static/index.html	前端页面（推荐）
# http://localhost:8000/users	获取用户列表（API）
# ✅ 推荐访问：http://localhost:8000/static/index.html