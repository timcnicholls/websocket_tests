import asyncio
import logging
import tornado

from tornado.options import define, options
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self):

        handlers = [
            (r"/ws", WsEchoHandler),
            (r"/api", HttpEchoHandler)
        ]
        settings = dict()

        super().__init__(handlers, **settings)

class WsEchoHandler(WebSocketHandler):

    def open(self):
        logging.info("Opening new WS connection from %r", self.request.host)

    def on_close(self):
        logging.info("Closing WS connection from %r", self)

    def on_message(self, message):
        self.write_message(message)

class HttpEchoHandler(RequestHandler):

    def get(self):
        self.write("hello, world")

    def put(self):
        self.write(self.request.body)

async def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
