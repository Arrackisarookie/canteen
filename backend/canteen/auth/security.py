from datetime import timedelta, datetime, timezone
from typing import Union

import bcrypt
from jose import jwt

from canteen.config import setting


def verify_password(plain_password: str, hashed_password: str):
    plain_password_byte_enc = plain_password.encode()
    hashed_password_byte_enc = hashed_password.encode()
    return bcrypt.checkpw(plain_password_byte_enc, hashed_password_byte_enc)


def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.SECRET_ALGORITHM)
    return encode_jwt
