import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.models.login_request import LoginRequest
from websocket import manager
from dotenv import load_dotenv
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


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

@app.post("/login")
async def login(request:LoginRequest):
    #1. 获取username和password
    username=request.username
    password=request.password
    #2. 查询user
    res=container.user_service.login_user(user_name=username,password=password)
    return res
@app.post("/file")
async def upload_file(file:UploadFile = File(...)):
    file_name=file.filename
    size=file.size
    content_type=file.headers.get("content-type")
    #接收到文件的时候需要把文件存储到以user_id的folder中
    return {"message":"upload success"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            print(f"收到客户端消息: {data}")

            await manager.send(
                websocket,
                f"Server: You said -> {data}"
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("客户端断开连接")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        app_dir="src"
    )