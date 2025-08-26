# 第一阶段：构建阶段（编译依赖）
FROM python:3.13-slim as builder

# 安装构建工具链
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 安装构建依赖（分离纯 Python 依赖）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段：运行阶段（最小化镜像）
FROM python:3.13-slim

# 安全加固：创建非 root 用户
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    mkdir /app && chown appuser:appgroup /app

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码（最后一步以利用缓存）
COPY --chown=appuser:appgroup . .

# 暴露端口
EXPOSE 8000

# 安全加固：限制文件权限
RUN chmod 755 /app && \
    find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \;

# 切换非特权用户
USER appuser

# 启动命令（带健康检查）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]