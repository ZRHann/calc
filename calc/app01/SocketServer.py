#!/usr/bin/env python

import asyncio

import websockets


async def handler(websocket):
    async for message in websocket:
        print("收到信息："+message)
    async for i in range(0, 100):
        websocket.send(str(i))



async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())