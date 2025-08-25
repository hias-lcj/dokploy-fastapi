# 使用官方Python基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 暴露端口
EXPOSE 8000

# 运行命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]