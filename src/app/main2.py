import httpx
import uvicorn
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- CopilotKit 核心引入 ---
from copilotkit import CopilotKitRemoteEndpoint, Action, Parameter
import copilotkit
from copilotkit.integrations.fastapi import add_fastapi_endpoint

from app.agent_main import MainAgent
from app.models.login_request import LoginRequest
from utils.token_util import TokenUtil
from utils.container import container

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# 1. 帮助函数：从 CopilotKit 请求头中解析 Token 并获取 user_id
# ------------------------------------------------------------------
def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """从 Authorization Header 中解析 user_id"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        decoded = TokenUtil.decode_token(token)
        return decoded['id']
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# ------------------------------------------------------------------
# 2. 将 MainAgent 包装为 CopilotKit Action / Agent 逻辑
# ------------------------------------------------------------------
# 如果你的 MainAgent 能够提供特定能力，可以注册为 Copilot Action
async def handle_agent_chat(message: str, properties: dict):
    """
    CopilotKit 处理函数
    properties 中包含了前端发来的 context 以及 request 信息
    """
    # 尝试从请求头或 properties 获取 token / user_id
    # CopilotKit 会把前端的 headers 传到 context/properties 中
    user_id = properties.get("user_id", "default_user")

    agent = MainAgent(user_id)

    # 将 MainAgent 的流式输出拼接或透传给 CopilotKit
    full_response = ""
    async for chunk in agent.stream_async(message):
        # 如果 MainAgent chunk 返回的是对象/字典，取 content
        content = getattr(chunk, 'content', str(chunk))
        full_response += content

    return full_response


# 定义 expose 给前端 CopilotKit 的 Actions
sdk = CopilotKitRemoteEndpoint(
    actions=[
        Action(
            name="chat_with_agent",
            description="与主 AI Agent 进行对话交互，处理用户业务请求",
            handler=handle_agent_chat,
            parameters=[
                {
                    "name": "message",
                    "type": "string",
                    "description": "用户输入的指令或消息内容",
                    "required": True
                }
            ]
        )
    ]
)

# ------------------------------------------------------------------
# 3. 挂载 CopilotKit Runtime 端点到 FastAPI
# ------------------------------------------------------------------
# 前端 v2 CopilotKit 的 runtimeUrl 将配置为: http://<your-host>:8080/copilotkit
add_fastapi_endpoint(app, sdk, "/copilotkit")


# ------------------------------------------------------------------
# 4. 原有业务 API 保持不变
# ------------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Hello FastAPI with CopilotKit v2"}


@app.get("/upload_url")
async def get_upload_url(file_name: str, user_id: str):
    file_service = container.file_service
    return file_service.create_upload_url(file_name, user_id)


@app.post("/login")
async def login(request: LoginRequest):
    username = request.username
    password = request.password
    res = container.user_service.login_user(user_name=username, password=password)
    return res


@app.post("/file")
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    size = file.size
    content_type = file.headers.get("content-type")
    return {"message": "upload success"}


# 注：原 /ws 端点可以保留作为备用，但 CopilotKit 前端通信将走 /copilotkit 端点。

if __name__ == "__main__":
    uvicorn.run(
        "app.main2:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )