from fastapi import FastAPI, status, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取环境变量，如果不存在则使用默认值
APP_TITLE = os.getenv("APP_TITLE", "Qinsong MS API")

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


@app.get("/")
async def root():
    return {
        "name": APP_TITLE,
        "description": f"{APP_TITLE} Service"
    }


@app.get("/api")
async def get_api_root(
    colour: Optional[str] = Query(None, description="颜色参数"),
    name: Optional[str] = Query(None, description="名称参数"),
    x_custom_header: Optional[str] = Header(None, description="自定义请求头")
):
    return {
        "code": 200,
        "data": {
            "colour": colour or "red",
            "name": name or "dafeng",
            "header_value": x_custom_header
        }
    }


@app.post("/api")
async def post_api_root(
    request: ApiRequest,
    x_custom_header: Optional[str] = Header(None, description="自定义请求头")
):
    return {
        "code": 200,
        "data": {
            "colour": request.colour or "red",
            "name": request.name or "dafeng",
            "header_value": x_custom_header
        }
    }


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