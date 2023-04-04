from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute


async def websocket_endpoint(websocket: WebSocket):
    client = websocket.client.host + ":" + str(websocket.client.port)
    print(f"Connected to Client: {client}")
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect as exc:
            print(f"Loss of connection to the client {client}")
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
    WebSocketRoute('/ws', websocket_endpoint),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
