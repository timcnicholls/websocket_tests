import asyncio
import websockets
import websockets.exceptions

async def hello(websocket):
    
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            break

        await websocket.send(message)

async def main():
    async with websockets.serve(hello, "127.0.0.1", 8890):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
