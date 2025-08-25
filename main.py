# # main.py
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.staticfiles import StaticFiles  
# from routers import router
# from models import create_users_table

# app = FastAPI(title="FastAPI MySQL 示例", version="1.0")

# # 启动时创建表
# @app.on_event("startup")
# def startup_event():
#     create_users_table()

# # ✅ 先注册 API 路由
# app.include_router(router)

# # ✅ 再挂载静态文件，使用 /static 前缀
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # ✅ 添加根路径，返回 index.html
# @app.get("/")
# def read_root():
#     return {"message": "欢迎使用 FastAPI + MySQL 示例 API", "docs": "/docs", "frontend": "/static/index.html"}

# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router
from routers_rds import router as rds_router  # 新增
from models import create_users_table

app = FastAPI(title="FastAPI 多数据库示例", version="1.0")

@app.on_event("startup")
def startup_event():
    create_users_table()

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