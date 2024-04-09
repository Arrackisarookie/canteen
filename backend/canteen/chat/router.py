from faker import Faker
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from backend.canteen.chat.schema import Room, User, Message

room = Room("main")
fake = Faker(["zh_CN"])

router = APIRouter()


@router.get("/fake/name")
async def get_fake_name():
    return {"nickname": fake.name()}


@router.websocket("/chatroom")
async def websocket_endpoint(websocket: WebSocket, nickname: str):
    await room.connect_manager.connect(websocket)
    user = User(nickname, websocket)
    await room.welcome(user)

    try:
        while True:
            content = await websocket.receive_text()
            message = Message(user, content)
            await room.broadcast(message)
    except WebSocketDisconnect:
        await room.farewell(user)
