# Qinsong MS API

一个基于 FastAPI 的简单后端服务。

## 环境变量配置

创建 `.env` 文件来配置环境变量：

```bash
# 应用标题
APP_TITLE=Qinsong MS API

# 第三方接口配置
THIRD_PARTY_URL=https://demo-01.com/api
THIRD_PARTY_METHOD=GET
THIRD_PARTY_HEADERS={"Authorization": "Bearer token"}
THIRD_PARTY_PARAMS={"key": "value"}
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
docker run -d -p 8000:8000 \
  -e APP_TITLE="Custom API Title" \
  -e THIRD_PARTY_URL="https://demo-01.idc.jieay.top/api" \
  -e THIRD_PARTY_METHOD="GET" \
  -e THIRD_PARTY_HEADERS='{"Authorization": "Bearer token"}' \
  -e THIRD_PARTY_PARAMS='{"key": "value"}' \
  qinsong-ms
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
    "name": "Qinsong MS API",
    "description": "Qinsong MS API Service"
}
```

### API 路由
#### GET 方法
- 端点：`GET /api`
- 查询参数：
  - `colour`: 颜色参数（可选）
  - `name`: 名称参数（可选）
- 请求头：所有请求头都会被返回
- 响应示例：
```json
{
    "code": 200,
    "data": {
        "colour": "blue",  // 如果提供了colour参数，否则默认为"red"
        "name": "custom",  // 如果提供了name参数，否则默认为"dafeng"
        "headers": {       // 所有请求头
            "user-agent": "curl/7.64.1",
            "accept": "*/*",
            "x-custom-header": "value"
        }
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
- 请求头：所有请求头都会被返回
- 响应示例：
```json
{
    "code": 200,
    "data": {
        "colour": "blue",  // 如果提供了colour参数，否则默认为"red"
        "name": "custom",  // 如果提供了name参数，否则默认为"dafeng"
        "headers": {       // 所有请求头
            "user-agent": "curl/7.64.1",
            "accept": "*/*",
            "content-type": "application/json",
            "x-custom-header": "value"
        }
    }
}
```

### 第三方接口调用
- 端点：`POST /three-party`
- 查询参数：所有查询参数都会被转发到第三方接口
- 请求头：除了以下headers外，所有请求头都会被转发到第三方接口
  - host
  - content-length
  - content-type
- 请求体（可选）：
```json
{
    "url": "https://demo-01.idc.jieay.top/api",  // 可选，默认使用环境变量配置
    "method": "GET",                              // 可选，默认使用环境变量配置
    "headers": {                                  // 可选，默认使用环境变量配置
        "Authorization": "Bearer token"
    },
    "params": {                                   // 可选，默认使用环境变量配置
        "key": "value"
    }
}
```
- 参数合并规则：
  1. 查询参数 + 环境变量参数 + 请求体参数
  2. 原始请求头 + 环境变量请求头 + 请求体请求头
- 响应：直接返回第三方接口的响应内容
- 错误处理：
  - 如果第三方接口调用失败，返回 502 错误
  - 如果响应不是 JSON 格式，返回原始文本内容

### 健康检查
- 端点：`GET /health`
- 响应示例：
```json
{
    "status": "healthy",
    "timestamp": "2024-02-14T12:00:00.000Z",
    "service": "Qinsong MS API"
}
```

Docker 容器已配置健康检查，每30秒检查一次服务状态。 