import asyncio


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        # print('<<', request)
        response = str(request)
        writer.write(response.encode('utf8'))
        # print('>>', response)
        await writer.drain()
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15555)
    
    addresses = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addresses}')
    
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
