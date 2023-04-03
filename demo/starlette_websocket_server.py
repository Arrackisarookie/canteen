from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles


def homepage(request):
    return PlainTextResponse('Hello, world!')


def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)


def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)


async def websocket_endpoint(websocket: WebSocket):
    client = websocket.client.host + ":" + str(websocket.client.port)
    print(f"Connected to Client: {client}")
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect as exc:
            print(f"Lost connection with Client: {client}")
            break
        print(f"<<< {data}")
        if data == 'quit':
            await websocket.close()
            print(f"Disconnected to Client: {client}")
            break
        await websocket.send_text(data)


def startup():
    print('Ready to go')


routes = [
    Route('/', homepage),
    Route('/user/me', user_me),
    Route('/user/{username}', user),
    WebSocketRoute('/ws', websocket_endpoint),
    Mount('/static', StaticFiles(directory="static")),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
