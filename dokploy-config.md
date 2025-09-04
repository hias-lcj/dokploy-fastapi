# Dokploy 部署配置指南

## 环境变量配置

在 Dokploy 中设置以下环境变量：

### 数据库配置
```
HOST=111.231.24.125
USER=linchengjun000@163.com
PASSWORD==*******************
DATABASE=mysqldb
PORT=3306

NEW_HOST=118.89.191.188
NEW_USER=mysql11889191188
NEW_PASSWORD=*******************
NEW_DATABASE=mysql11889191188
NEW_PORT=3306

RDS_HOST=rm-uf6io467mc774dvy6ho.mysql.rds.aliyuncs.com
RDS_USER=g-dev
RDS_PASSWORD==*******************
RDS_DATABASE=h_xingzhi
```

### LLM配置
```
OPENAI_API_KEY=sk-=*******************
OPENAI_API_BASE_URL=https://api.siliconflow.cn/v1
LLM_MODEL=Qwen/Qwen3-8B
```

## 部署步骤

1. 在 Dokploy 中创建新项目
2. 连接你的 Git 仓库
3. 设置环境变量（如上所示）
4. 确保端口设置为 8000
5. 部署应用

## 故障排除

### 检查健康状态
访问 `https://your-domain.com/health` 检查服务状态

### 检查API文档
访问 `https://your-domain.com/docs` 查看API文档

### 常见问题
1. 数据库连接失败：检查环境变量是否正确设置
2. 404错误：确保路由配置正确
3. JSON解析错误：检查API响应格式

## 网络配置

确保 Dokploy 服务器可以访问：
- 数据库服务器（端口 3306）
- SiliconFlow API（端口 443）
