with open("resource/index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

with open("resource/pages/login.html", "r", encoding="utf-8") as f:
    signin_html = f.read()


SECRET_KEY = "c627dcc5873ec9866fe6e02ee97fcad95417906df67a687cda1ccb18a9aca0f8"
SECRET_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
