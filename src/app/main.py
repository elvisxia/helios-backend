import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile

from websocket import manager
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

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