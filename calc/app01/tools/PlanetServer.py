#!/usr/bin/env python

import asyncio
import time

import websockets
import json

USERS = {}
'''
{
    "user1": {
        "websocket": ws, 
        "ball": ball, 
    }
    
    "user2": {
        "websocket": ws, 
        "ball": ball, 
    }
}
'''

class Ball:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.m = 1.0
        self.color = 0
        self.radius = 20.0
        self.onWdown = False
        self.onAdown = False
        self.onSdown = False
        self.onDdown = False


async def board(msg):
    for username, ws in USERS.items():
        print(1)
        await ws.send(msg)


async def handler(websocket):
    async for message in websocket:
        print("接收到" + str(message))
        data = json.loads(message)
        if data["type"] == "AddBall":
            # 给他每一个球的状态, 广播他的状态
            USERS[data["username"]] = {}
            USERS[data["username"]]["websocket"] = websocket
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
