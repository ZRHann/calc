#!/usr/bin/env python

import asyncio
import time

import websockets
import json

USERS = {}


async def board(msg):
    for username, ws in USERS.items():
        print(1)
        await ws.send(msg)


async def handler(websocket):
    async for message in websocket:
        print("接收到" + str(message))
        data = json.loads(message)
        if data["type"] == "login":
            # 给他每一个球的状态, 广播他的状态
            USERS[data["username"]] = websocket
            msg = {
                "type": "AddBall",
                "username": data["username"],
                "content": '',
            }
            await board(json.dumps(msg))
        elif data["type"] == "DeleteBall":
            msg = {
                "type": "logout",
                "username": data["username"],
                "content": '',
            }
            USERS.pop(data["username"])
            print(USERS)
            await board(json.dumps(msg))
        elif data["type"] == "Update":
            msg = {
                "type": "send",
                "username": data["username"],
                "content": data["content"],
            }
            await board(json.dumps(msg))


async def main():
    async with websockets.serve(handler, "172.31.0.132", 9999):
        print("服务端已启动")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
