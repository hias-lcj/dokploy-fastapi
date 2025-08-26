# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router
from routers_rds import router as rds_router  # 新增
from models import create_users_table
import uvicorn
import webbrowser
import threading

app = FastAPI(title="FastAPI 多数据库示例", version="1.0")

@app.on_event("startup")
def startup_event():
    create_users_table()
    # 在新线程中打开前端页面，避免阻塞应用启动
    threading.Thread(target=lambda: webbrowser.open("http://localhost:8000/static/index.html")).start()


# ✅ 注册 API 路由
app.include_router(router)
app.include_router(rds_router)  # 新增：RDS 路由

# ✅ 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {
        "message": "多数据库 FastAPI 服务",
        "docs": "/docs",
        "local_users": "/users",
        "rds_users": "/rds/users",
        "frontend": "/static/index.html"
    }

if __name__ == "__main__":
    # 运行 Uvicorn 服务器
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
#     地址	用途
# http://localhost:8000	查看 API 信息
# http://localhost:8000/docs	Swagger 文档
# http://localhost:8000/static/index.html	前端页面（推荐）
# http://localhost:8000/users	获取用户列表（API）
# ✅ 推荐访问：http://localhost:8000/static/index.html