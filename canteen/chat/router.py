from faker import Faker
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from canteen.chat.schema import Room, User, Message

room = Room("main")
fake = Faker(["zh_CN"])

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"username": "TestUser"}
    )


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
