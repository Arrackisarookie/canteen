from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from canteen.auth.router import router as auth_router
from canteen.chat.router import router as chat_router

origins = [
    "http://localhost:8000",
    "https://chat.aiar.site",
    "https://canteen-three.vercel.app",
]


app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(chat_router, tags=["Chat"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
