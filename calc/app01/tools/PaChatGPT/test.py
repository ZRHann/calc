from asyncChatGPT.asyncChatGPT import Chatbot
import asyncio
config = {
            # "email": "2829442630@qq.com",
            # "password": "zg801zrh160118.",
            # Deprecated. Use only if you encounter captcha with email/password
            # "proxy": "<HTTP/HTTPS_PROXY>"
            "session_token": ""
        }
with open("session_token.txt", "r") as f:
    config["session_token"] = f.read()
chatbot = Chatbot(config, conversation_id=None)
print("connected")


async def f1():
    res = await chatbot.get_chat_response("who are you", output="stream")
    async for r in res:
        await asyncio.sleep(0.02)
        print(r["message"])


async def f2():
    res = await chatbot.get_chat_response("123", output="stream")
    async for r in res:
        await asyncio.sleep(0.02)
        print(r["message"])


async def main():
    task1 = asyncio.create_task(f1())
    task2 = asyncio.create_task(f2())
    await task1
    await task2

asyncio.run(main())



