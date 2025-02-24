import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://127.0.0.1:5000/ws") as ws:
        while True:
            msg = await ws.recv()
            print("Received:", msg)

asyncio.run(listen())
