#!/usr/bin/env python

import asyncio
import json
import time

import aiohttp
import requests
import websockets

from tornado.options import define, options
from tornado.websocket import websocket_connect
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


define("host", default="127.0.0.1", help="Server host")
define("port", default=8888, help="Server port", type=int)
define("num_msgs", default=1000, help="number of messages to send", type=int)
define("no_http", default=False, help="Do not run HTTP connections", type=bool)

async def tornado_ws_client(uri):

    ws = await websocket_connect(uri)

    start = time.time()

    for idx in range(options.num_msgs):

        message = {"body": "hello, world!", "idx": idx}
        ws.write_message(json.dumps(message))

        reply = await ws.read_message()
        assert json.loads(reply) == message

    end = time.time()
    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"Tornado websocket: sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

async def pyws_ws_client(uri):

    async with websockets.connect(uri) as ws:

        start = time.time()

        for idx in range(options.num_msgs):
            message = {"body": "hello, world!", "idx": idx}
            await ws.send(json.dumps(message))
            response = await ws.recv()
            assert json.loads(response) == message

    end = time.time()
    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"Python websocket : sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

async def aio_ws_client(uri):

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(uri) as ws:

            start = time.time()

            for idx in range(options.num_msgs):

                message = {"body": "hello, world!", "idx": idx}
                await ws.send_json(message)
                response = await ws.receive_json()
                assert response == message

    end = time.time()

    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"AIO websocket : sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

async def tornado_http_client(uri):

    http = AsyncHTTPClient()
    request = HTTPRequest(url=uri, method="PUT")

    start = time.time()

    for idx in range(options.num_msgs):

        message = {"body": "hello, world!", "idx": idx}
        request.body = json.dumps(message)
        response = await http.fetch(request)
        assert json.loads(response.body) == message

    end = time.time()
    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"Tornado HTTP PUT : sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

def requests_client(uri):

    with requests.Session() as session:
        start = time.time()

        for idx in range(options.num_msgs):

            message = {"body": "hello, world!", "idx": idx}
            response = session.put(uri, json=message)
            assert response.json() == message

    end = time.time()
    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"Requests HTTP PUT : sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

async def aio_http_client(uri):

    async with aiohttp.ClientSession() as client:

        start = time.time()

        for idx in range(options.num_msgs):

            message = {"body": "hello, world!", "idx": idx}
            response = await client.put(uri, json=message)
            reply = await response.text()
            assert json.loads(reply) == message

    end = time.time()
    delta = end - start
    rate = float(options.num_msgs) / delta
    print(f"AIO HTTP PUT : sent and received {options.num_msgs} messages in {delta:.2f} secs, rate = {rate:.2f} Hz")

def main():

    options.parse_command_line()

    ws_uri = f"ws://{options.host}:{options.port}/ws"
    http_uri = f"http://{options.host}:{options.port}/api"

    asyncio.run(tornado_ws_client(ws_uri))
    asyncio.run(pyws_ws_client(ws_uri))
    asyncio.run(aio_ws_client(ws_uri))
    if not options.no_http:
        asyncio.run(tornado_http_client(http_uri))
        requests_client(http_uri)
        asyncio.run(aio_http_client(http_uri))

if __name__ == '__main__':
    main()