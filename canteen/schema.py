import reprlib
from datetime import datetime
from typing import Union

from starlette.websockets import WebSocket


class User:
    def __init__(
        self, username: str,
        ws_connection: Union[WebSocket, None] = None
    ):
        self.username: str = username
        self.ws_connection: Union[WebSocket, None] = ws_connection


class Message:
    def __init__(self, user: User, content: str, create_time: datetime = datetime.now()):
        self.user: User = user
        self.content: str = content
        self.create_time: datetime = create_time

    def json(self):
        return {
            "user": self.user.username,
            "content": self.content,
            "create_time": self.create_time.strftime("%c")
        }

    def __repr__(self):
        return reprlib.repr(self.json())


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    @staticmethod
    async def close(websocket: WebSocket):
        await websocket.close()


class Room:
    def __init__(self, room_id: str):
        self.room_id: str = room_id
        self.users: list[User] = []
        self.messages: list[Message] = []
        self.connect_manager = ConnectionManager()
        self.compere = User(f"Room_{room_id}")

    async def broadcast(self, message: Union[str, Message]):
        if not isinstance(message, Message):
            message = Message(self.compere, message)
        await self.connect_manager.broadcast(message.json())

    async def send_to(self, user: User, message: Union[str, Message]):
        if not isinstance(message, Message):
            message = Message(self.compere, message)
        await self.connect_manager.send_personal_message(user.ws_connection, message.json())

    async def welcome(self, user: User):
        self.add_user(user)

        content = f"{user.username} enter the room {self.room_id}"
        await self.broadcast(content)

        content = f"Welcome, {user.username}! You have joined the room: {self.room_id}"
        await self.send_to(user, content)

    async def farewell(self, user: User):
        self.disconnect(user.ws_connection)
        content = f"User {user.username} left the room"
        await self.broadcast(content)

    def disconnect(self, websocket: WebSocket):
        self.connect_manager.disconnect(websocket)

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_user(self, user: User):
        self.users.append(user)

    def close(self):
        for user in self.users:
            self.connect_manager.close(user.ws_connection)
