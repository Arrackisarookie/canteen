from faker import Faker
from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from canteen.chat.schema import Room, User, Message
from canteen.config import index_html

room = Room("main")
fake = Faker(["zh_CN"])

router = APIRouter()


@router.get("/")
async def index():
    return HTMLResponse(index_html)


@router.get("/faker/name")
async def get_fake_name():
    return fake.name()


@router.websocket("/room/main")
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
