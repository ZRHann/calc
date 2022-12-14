from revChatGPT.revChatGPT import AsyncChatbot as Chatbot
import asyncio
config = {
            # "email": "2829442630@qq.com",
            # "password": "zg801zrh160118.",
            # Deprecated. Use only if you encounter captcha with email/password
            # "proxy": "<HTTP/HTTPS_PROXY>"
            "session_token": "",
            # "cf_clearance": "",
            # "user_agent": "",
        }

with open("session_token.txt", "r") as f:
    config["session_token"] = f.read()

print(config)
chatbot = Chatbot(config)
print("connected")


async def f1(msg):
    res = await chatbot.get_chat_response(msg, output="stream")
    async for r in res:
        print(r["message"])


async def main():
    while True:
        msg = input()
        await f1(msg)

asyncio.run(main())



