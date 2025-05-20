from fastapi import FastAPI, status, Header, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
import json

# 加载环境变量
load_dotenv()

# 获取环境变量，如果不存在则使用默认值
APP_TITLE = os.getenv("APP_TITLE", "Qinsong MS API")

# 第三方接口配置
THIRD_PARTY_URL = os.getenv("THIRD_PARTY_URL", "https://demo-01.com/api")
THIRD_PARTY_METHOD = os.getenv("THIRD_PARTY_METHOD", "GET")
THIRD_PARTY_HEADERS = json.loads(os.getenv("THIRD_PARTY_HEADERS", "{}"))
THIRD_PARTY_PARAMS = json.loads(os.getenv("THIRD_PARTY_PARAMS", "{}"))

app = FastAPI(title=APP_TITLE)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiRequest(BaseModel):
    colour: Optional[str] = None
    name: Optional[str] = None


class ThirdPartyRequest(BaseModel):
    url: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    return {
        "name": APP_TITLE,
        "description": f"{APP_TITLE} Service"
    }


@app.get("/api")
async def get_api_root(
    request: Request,
    colour: Optional[str] = Query(None, description="颜色参数"),
    name: Optional[str] = Query(None, description="名称参数")
):
    # 获取所有请求头
    headers = dict(request.headers)
    return {
        "code": 200,
        "data": {
            "colour": colour or "red",
            "name": name or "dafeng",
            "headers": headers
        }
    }


@app.post("/api")
async def post_api_root(
    request: Request,
    api_request: ApiRequest
):
    # 获取所有请求头
    headers = dict(request.headers)
    return {
        "code": 200,
        "data": {
            "colour": api_request.colour or "red",
            "name": api_request.name or "dafeng",
            "headers": headers
        }
    }


@app.post("/three-party")
async def call_third_party(request: Request, third_party_request: Optional[ThirdPartyRequest] = None):
    """
    调用第三方接口
    """
    try:
        # 获取原始请求的headers
        original_headers = dict(request.headers)
        # 移除一些不需要转发的headers
        headers_to_remove = [
            'host', 'content-length', 'content-type', 'user-agent', 'accept', 'accept-encoding', 'connection'
        ]
        for header in headers_to_remove:
            original_headers.pop(header, None)

        # 获取查询参数
        query_params = dict(request.query_params)

        # 使用请求中的配置或环境变量中的默认配置
        url = third_party_request.url if third_party_request and third_party_request.url else THIRD_PARTY_URL
        method = third_party_request.method if third_party_request and third_party_request.method else THIRD_PARTY_METHOD
        
        # 合并headers：原始请求headers + 配置的headers
        headers = {**original_headers}
        if third_party_request and third_party_request.headers:
            headers.update(third_party_request.headers)
        elif THIRD_PARTY_HEADERS:
            headers.update(THIRD_PARTY_HEADERS)

        # 合并参数：查询参数 + 配置的参数
        params = {**query_params}
        if third_party_request and third_party_request.params:
            params.update(third_party_request.params)
        elif THIRD_PARTY_PARAMS:
            params.update(THIRD_PARTY_PARAMS)

        # 发送请求
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params if method.upper() == "GET" else None,
            json=params if method.upper() != "GET" else None
        )

        # 尝试解析JSON响应
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"content": response.text}

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Third party API error: {str(e)}"
        )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    健康检查接口
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": APP_TITLE
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 