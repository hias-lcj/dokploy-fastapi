# 多数据库 + LLM 管理系统

这是一个基于 FastAPI 的多数据库管理系统，集成了大模型 API 功能。当前版本已完成项目结构重构，模块职责更清晰、可维护性更强。

## 变化概览（重要）
- 新增 `app/` 分层目录：`core/`（配置）、`db/`（数据库连接）、`services/`（领域服务）、`api/routers/`（路由）
- 统一数据库访问：新增 `app/db/mysql.py` 提供主库与新库的连接接口。
- LLM 服务迁移：`llm_service.py` 替换为 `app/services/llm.py` 并通过 `app/api/routers/llm.py` 暴露接口。
- 路由拆分：原 `routers.py`、`routers_new.py`、`routers_llm.py`、`routers_rds.py` 已对应迁移到 `app/api/routers/` 下。
- 保留了原有的 `models.py`、`models_new.py` 用于初始化建表（后续可迁移到 `app/models/`）。

建议后续删除或停用以下旧文件，避免混淆（如已有外部引用可暂缓删除）：
- `routers.py`、`routers_new.py`、`routers_llm.py`、`routers_rds.py`
- `llm_service.py`
- `database_new.py`

> 注意：`database.py`（主库）与 `database_rds.py`（只读库）仍保留以兼容现有建表逻辑和 RDS 依赖。新开发尽量统一使用 `app/db/mysql.py`。

## 新目录结构
```
fastapi/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── config.py         # 环境与全局配置
│   ├── db/
│   │   ├── __init__.py
│   │   └── mysql.py          # 主库/新库连接（统一入口）
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm.py            # 大模型服务
│   └── api/
│       ├── __init__.py
│       └── routers/
│           ├── __init__.py
│           ├── users.py      # 用户：主库
│           ├── newdb.py      # 产品/订单：新库
│           ├── rds.py        # 只读 RDS
│           └── llm.py        # LLM 对话
├── main.py                   # 应用入口（已接入新结构）
├── static/
│   └── index.html            # 前端页面（含 LLM 与新库 UI）
├── models.py                 # 主库建表（保留）
├── models_new.py             # 新库建表（保留）
├── database.py               # 主库连接（兼容保留）
├── database_rds.py           # RDS 连接（保留）
├── requirements.txt
└── README.md
```

## 环境配置
将环境变量写入项目根目录下的 `.env`（或系统环境变量）：
```
# 主库
HOST=localhost
USER=root
PASSWORD=your_password
DATABASE=your_database
PORT=3306

# 新库（若不填则默认复用主库连接参数）
NEW_HOST=localhost
NEW_USER=root
NEW_PASSWORD=your_new_password
NEW_DATABASE=newdb
NEW_PORT=3306

# LLM
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE_URL=https://api.openai.com/v1
LLM_MODEL=Qwen/Qwen3-8B
```

## 安装依赖
```
pip install -r requirements.txt
```

## 运行
```
python main.py
# 或
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 访问
- 前端页面：/static/index.html （例如 `http://localhost:8000/static/index.html`）
- API 文档：/docs
- 根路由：/

## API 端点（新结构）
- 用户（主库）：
  - GET `/users`
  - POST `/users`
- 新库（产品/订单）：
  - GET `/newdb/products`，POST `/newdb/products`
  - GET `/newdb/orders`，POST `/newdb/orders`
- RDS（只读）：
  - GET `/rds/users`
- LLM：
  - POST `/llm/chat`
  - GET `/llm/prompts`
  - GET `/llm/health`

## 重构建议与下一步优化
- 将 `models.py`、`models_new.py` 迁移至 `app/models/` 并统一建表入口（例如 `app/db/migrate.py`）。
- 废弃 `database.py` 与 `database_new.py`，统一引用 `app/db/mysql.py` 的 `get_primary_db` 和 `get_secondary_db`。
- 为 Pydantic 模型和响应体建立 `app/schemas/`，将 `schemas.py`、`schemas_new.py` 合并并模块化。
- 引入依赖注入/仓储模式（Repository Pattern），把 SQL 从路由中下沉到 `app/repositories/`。
- 增加测试目录 `tests/`，覆盖服务与路由。
- 生产环境建议关闭自动打开浏览器，增加 CORS、安全头配置。

## 常见问题
- LLM 初始化失败：检查 `OPENAI_API_KEY` 和 `OPENAI_API_BASE_URL`。
- 新库/主库连接失败：确认数据库服务和权限，并核对 `.env`。
- RDS 接口报错：确认安全组与白名单，核对 `database_rds.py` 的连接信息。

## 贡献
欢迎提交 Pull Request 或 Issue，共同改进项目。
