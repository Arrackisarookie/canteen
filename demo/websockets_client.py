#!/usr/bin/env python

import asyncio
import time

import websockets


async def hello():
    start_time = time.time()
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        print("Connected to the websocket server.")
        while True:
            message = input(">>> ")
            if message == "quit":
                await websocket.send("Bye!")
                break
            await websocket.send(message)
            print(await websocket.recv())
    print(f"Cost seconds: {time.time() - start_time:.6f}")


asyncio.run(hello())
