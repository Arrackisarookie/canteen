from fastapi import FastAPI
from starlette import status
from starlette.exceptions import WebSocketException
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect, WebSocket

from canteen.model import User, Message
from canteen.config import index_html, signin_html, rooms


app = FastAPI()
app.mount("/assets", StaticFiles(directory="resource/assets"), name="assets")


@app.get("/")
async def index():
    return HTMLResponse(index_html)


@app.get("/login")
async def login():
    return HTMLResponse(signin_html)


@app.websocket("/{room_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str
):
    if room_id not in rooms:
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)
    room = rooms[room_id]

    await room.connect_manager.connect(websocket)
    user = User(user_id, websocket)
    await room.welcome(user)

    try:
        while True:
            content = await websocket.receive_text()
            message = Message(user, content)
            await room.broadcast(message)
    except WebSocketDisconnect:
        await room.farewell(user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
