from pydantic_settings import BaseSettings


class AppSetting(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    SECRET_KEY: str
    SECRET_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15


setting = AppSetting()


with open("resource/index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

with open("resource/pages/login.html", "r", encoding="utf-8") as f:
    signin_html = f.read()


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$GZIBoVl.LIAXeJMH1Ugoku3CWnAuRlgD9BIEZ79PkAJhg9jGVVgFe",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$K.m/ITR9H2.CiAIovHQmBusvExg9zwWdDCrD05YwwYYYwaipkEv46",
        "disabled": True,
    },
}
