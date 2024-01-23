
import argparse

from aiohttp import web, WSMsgType

class HttpEchoHandler():

    def __init__(self):
        pass

    async def get(self, request: web.Request) -> web.StreamResponse:
        return web.Response(text="hello, world")

    async def put(self, request: web.Request) -> web.StreamResponse:
        message = await request.json()
        return web.json_response(message)

class WsEchoHandler():

    def __init__(self):
        pass

    async def handle(self, request):

        print("ws connection opening")

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await ws.send_str(message.data)
            elif message.type == WSMsgType.ERROR:
                print(f"ws connection closed with exception {ws.exception()}")

        print("ws connection closed")
        return ws

def main():

    parser = argparse.ArgumentParser(description="aiohttp server for websocket testing")
    parser.add_argument('--host', default='127.0.0.1', type=str, help="Server host address")
    parser.add_argument('--port', default=8889, type=int, help='Server port')
    args = parser.parse_args()

    app = web.Application()

    http_handler = HttpEchoHandler()
    ws_handler = WsEchoHandler()

    app.add_routes([
        web.get('/api', http_handler.get),
        web.put('/api', http_handler.put),
        web.get('/ws', ws_handler.handle),
    ])
    web.run_app(app, host=args.host, port=args.port)

if __name__ == '__main__':
    main()
