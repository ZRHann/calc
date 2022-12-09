import asyncio

async def f1():
    print(1)
    await asyncio.sleep(1)
    print(11)


async def f2():
    while True:
        pass
        # await asyncio.sleep(1)
        # print(22)


async def main():
    task1 = asyncio.create_task(f1())
    task2 = asyncio.create_task(f2())
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
