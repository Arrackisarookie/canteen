from faker import Faker
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect, WebSocket

from canteen.schema import User, Message, Room
from canteen.config import index_html
from canteen.auth.router import router as auth_router


app = FastAPI()
app.mount("/assets", StaticFiles(directory="resource/assets"), name="assets")

fake = Faker(["zh_CN"])

room = Room("main")


@app.get("/faker/name")
async def get_fake_name():
    return fake.name()


@app.get("/")
async def index():
    return HTMLResponse(index_html)


@app.websocket("/room/main")
async def websocket_endpoint(websocket: WebSocket):
    username = fake.name()
    await room.connect_manager.connect(websocket)
    user = User(username, websocket)
    await room.welcome(user)

    try:
        while True:
            content = await websocket.receive_text()
            message = Message(user, content)
            await room.broadcast(message)
    except WebSocketDisconnect:
        await room.farewell(user)


app.include_router(auth_router, tags=["Auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
