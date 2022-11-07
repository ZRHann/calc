#!/usr/bin/env python

import asyncio
import time

import websockets




async def msgSender(websocket, msg):
    await websocket.send(msg)


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print("收到："+message)
        await msgSender(websocket, "hi")


async def main():
    async with websockets.serve(handler, "172.31.0.132", 9999):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
