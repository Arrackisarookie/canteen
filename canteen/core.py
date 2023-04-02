import asyncio
from typing import Set, List, Tuple

from uvicorn.protocols.websockets.websockets_impl import WebSocketProtocol


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.channels = []

    def subscribe(self, channel: "Channel") -> None:
        pass

    def unsubscribe(self, channel) -> None:
        pass

    def publish(self, channel, content) -> None:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"


class Channel:
    def __init__(self, name) -> None:
        self.name = name
        self.members = []
        self.records = []

    def broadcast(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"


class ServerState:
    """
    Shared servers state that is available between all protocol instances.
    """

    def __init__(self) -> None:
        self.total_requests = 0
        self.connections: Set["WebSocketProtocol"] = set()
        self.tasks: Set[asyncio.Task] = set()
        self.default_headers: List[Tuple[bytes, bytes]] = []


class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport: asyncio.Transport = None  # type: ignore[assignment]

    def connection_made(self, transport: asyncio.Transport):
        peer_name = transport.get_extra_info('peer_name')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def connection_lost(self, exc):
        print(exc)

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(lambda: EchoServerProtocol(), '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
