#!/usr/bin/env python

import asyncio
import time

import websockets
import json

USERS = {}


async def msgSender(msg):
    for k, v in USERS.items():
        print(1)
        await v.send(msg)


async def handler(websocket):
    async for message in websocket:
        print("接收到" + str(message))
        data = json.loads(message)
        if data["type"] == "login":
            USERS[data["username"]] = websocket
            msg = {
                "type": "login",
                "username": data["username"],
                "content": '',
            }
            await msgSender(json.dumps(msg))
        elif data["type"] == "logout":
            msg = {
                "type": "logout",
                "username": data["username"],
                "content": '',
            }
            USERS.pop(data["username"])
            print(USERS)
            await msgSender(json.dumps(msg))
        elif data["type"] == "send":
            msg = {
                "type": "send",
                "username": data["username"],
                "content": data["content"],
            }
            await msgSender(json.dumps(msg))


async def main():
    async with websockets.serve(handler, "172.31.0.255", 9999):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
