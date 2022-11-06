#!/usr/bin/env python

import asyncio
import time

import websockets


async def msgSender(websocket):
    for i in range(0, 100):
        print("sended "+str(i))
        websocket.send(str(i))
        time.sleep(1)






async def handler(websocket):
    asyncio.run(msgSender())
    async for message in websocket:
        print("收到信息："+message)




async def main():
    async with websockets.serve(handler, "172.31.0.132", 9999):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())