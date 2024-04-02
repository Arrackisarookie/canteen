from datetime import timedelta, datetime, timezone
from typing import Union

import bcrypt
from faker import Faker
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect, WebSocket

from canteen.model import UserModel, UserInDbModel, TokenData, Token
from canteen.schema import User, Message, Room
from canteen.config import index_html, fake_users_db, SECRET_KEY, SECRET_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()
app.mount("/assets", StaticFiles(directory="resource/assets"), name="assets")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
fake = Faker(["zh_CN"])

room = Room("main")


def verify_password(plain_password: str, hashed_password: str):
    plain_password_byte_enc = plain_password.encode()
    hashed_password_byte_enc = hashed_password.encode()
    return bcrypt.checkpw(plain_password_byte_enc, hashed_password_byte_enc)


def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDbModel(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECRET_ALGORITHM)
    return encode_jwt


async def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECRET_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )
    return current_user


@app.get("/faker/name")
async def get_fake_name():
    return fake.name()


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/user/me", response_model=UserModel)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
