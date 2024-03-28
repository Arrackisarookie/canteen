import json

from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws/chat/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, user_name: str):
    await websocket.accept()
    content = {
        "user_id": user_name,
        "message": f"Welcome, {user_name}! You have joined the room: {room_name}"
    }
    await websocket.send_text(json.dumps(content, ensure_ascii=False))

    while True:
        data = await websocket.receive_text()
        # 广播消息给其他连接到同一房间的所有客户端
        # 在实际应用中，你需要维护一个连接池或者使用类似Redis Pub/Sub的方式
        # 这里为了简化只演示接收消息的部分逻辑
        print(f"Message from {room_name}-{user_name}: {data}")


# 启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
