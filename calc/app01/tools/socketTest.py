#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://zrhan.cf:9999"
    async with websockets.connect(uri) as websocket:
        pass

if __name__ == "__main__":
    asyncio.run(hello())