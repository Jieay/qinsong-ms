# Qinsong MS API

一个基于 FastAPI 的简单后端服务。

## 环境变量配置

创建 `.env` 文件来配置环境变量：

```bash
# 应用标题
APP_TITLE=Qinsong MS API
```

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
python main.py
```

服务将在 http://localhost:8000 启动

## Docker 部署

1. 构建镜像：
```bash
docker build -t qinsong-ms .
```

2. 运行容器：
```bash
# 使用默认配置
docker run -d -p 8000:8000 qinsong-ms

# 使用自定义环境变量
docker run -d -p 8000:8000 -e APP_TITLE="Custom API Title" qinsong-ms
```

## API 文档

启动服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口说明

### 根路由
- 端点：`GET /`
- 响应示例：
```json
{
    "name": "qinsong-ms",
    "description": "Qinsong MS API Service"
}
```

### API 路由
#### GET 方法
- 端点：`GET /api`
- 查询参数：
  - `colour`: 颜色参数（可选）
  - `name`: 名称参数（可选）
- 请求头：
  - `x-custom-header`: 自定义请求头（可选）
- 响应示例：
```json
{
    "code": 200,
    "data": {
        "colour": "blue",  // 如果提供了colour参数，否则默认为"red"
        "name": "custom",  // 如果提供了name参数，否则默认为"dafeng"
        "header_value": "custom-header-value"  // 如果提供了x-custom-header，否则为null
    }
}
```

#### POST 方法
- 端点：`POST /api`
- 请求体：
```json
{
    "colour": "blue",  // 可选
    "name": "custom"   // 可选
}
```
- 请求头：
  - `x-custom-header`: 自定义请求头（可选）
- 响应示例：
```json
{
    "code": 200,
    "data": {
        "colour": "blue",  // 如果提供了colour参数，否则默认为"red"
        "name": "custom",  // 如果提供了name参数，否则默认为"dafeng"
        "header_value": "custom-header-value"  // 如果提供了x-custom-header，否则为null
    }
}
```

### 健康检查
- 端点：`GET /health`
- 响应示例：
```json
{
    "status": "healthy",
    "timestamp": "2024-02-14T12:00:00.000Z",
    "service": "qinsong-ms"
}
```

Docker 容器已配置健康检查，每30秒检查一次服务状态。 