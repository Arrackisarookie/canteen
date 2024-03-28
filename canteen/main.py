from starlette.websockets import WebSocketDisconnect
from fastapi import FastAPI, WebSocket

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, user_name: str):
    try:
        await manager.connect(websocket)
        content = {
            "user_id": "System",
            "message": f"Welcome, {user_name}! You have joined the room: {room_name}"
        }
        await websocket.send_json(content)

        while True:
            data = await websocket.receive_text()
            content = {
                "user_id": user_name,
                "message": f"{data}"
            }
            await manager.broadcast(content)
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        content = {
            "user_id": "System",
            "message": f"Client #{user_name} left the chat"
        }
        await manager.broadcast(content)


# 启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
