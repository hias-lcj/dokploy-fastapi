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
    """
    根路由处理函数
    返回服务的基本信息和可用端点列表
    
    Returns:
        dict: 包含服务信息和各种端点URL的字典
    """
    return {
        "message": "多数据库 + LLM FastAPI 服务",  # 服务描述信息
        "docs": "/docs",  # Swagger API文档地址
        "local_users": "/users",  # 本地用户数据库端点
        "rds_users": "/rds/users",  # RDS用户数据库端点
        "newdb_products": "/newdb/products",  #新产品数据库端点
        "newdb_orders": "/newdb/orders",  # 新订单数据库端点
        "llm_chat": "/llm/chat",  # LLM聊天服务端点
        "frontend": "/static/index.html",  # 前端页面地址
    }

if __name__ == "__main__":
    """
    程序入口点
    当直接运行此脚本时，启动FastAPI服务器
    
    参数说明:
        host: "0.0.0.0" 表示服务器监听所有可用的网络接口
        port: 8000 指定服务器运行的端口号
        reload: True 启用自动重载功能，代码修改后服务器会自动重启
    """
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# 以下是使用命令行启动FastAPI服务的命令示例：
# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 服务启动后可用的地址及其用途：
# http://localhost:8000          - 查看API基本信息
# http://localhost:8000/docs     - Swagger API文档界面
# http://localhost:8000/static/index.html  - 前端页面（推荐使用）
# http://localhost:8000/users    - 获取用户列表的API端点

# ✅ 推荐访问：http://localhost:8000/static/index.html
# 这个前端页面提供了完整的用户界面，可以方便地使用所有功能
