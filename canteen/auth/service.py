from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from starlette.exceptions import HTTPException

from canteen.auth.security import verify_password
from canteen.config import setting, fake_users_db
from canteen.model import UserInDbModel, TokenData, UserModel

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str) -> UserModel:
    if username in db:
        user_dict = db[username]
        return UserInDbModel(**user_dict)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.SECRET_ALGORITHM])
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


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )
    return current_user


def authenticate_user(fake_db, username: str, password: str) -> Union[UserModel, None]:
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
