from asyncChatGPT.asyncChatGPT import Chatbot
import asyncio
import time
import websockets
import json
import threading
import re
import pymysql


class MainClass:
    mychatbot = None
    sql = None


class SQL:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='zg801zrh160118.',
                                  database='ChatGPT_OL')
        self.cursor = self.db.cursor()

    def add_msg_json(self, msg_json):
        sql = "INSERT INTO conversation_log(msg_json) VALUES (\"{}\")".format(pymysql.converters.escape_string(msg_json))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            print("Successfully Added a msg_json to database")
        except Exception as ex:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Failed to Add a msg_json to database: ")
            print(ex)  # 打印异常信息

    def get_msg_json(self):
        sql = "SELECT * FROM conversation_log"

        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            print("Successfully get_msg_json")
            return results
        except Exception as ex:
            print("get_msg_json Error: unable to fetch data: ")
            print(ex)  # 打印异常信息
            return []


class MyChatBot:
    def __init__(self):
        config = {
            # "email": "<YOUR_EMAIL>",
            # "password": "<YOUR_PASSWORD>"#,
            "session_token": "",
            # Deprecated. Use only if you encounter captcha with email/password
            # "proxy": "<HTTP/HTTPS_PROXY>"
        }
        with open("session_token.txt", "r") as f:
            config["session_token"] = f.read()
        self.isThinking = False
        self.chatbot = Chatbot(config, conversation_id=None)
        self.question = ""
        print("connected")

    async def ask(self, server1):
        while True:
            await asyncio.sleep(0.3)
            if self.isThinking:
                print("Asked ChatGPT: ")
                print(self.question)
                response = await self.chatbot.get_chat_response(self.question, output="text")
                print("ChatGPT answered: ")
                print(response)
                msg1 = {
                    "type": "send",
                    "username": "ChatGPT",
                    "content": response["message"],
                }
                await server1.msgSender(json.dumps(msg1))
                self.isThinking = False


class Server:
    def __init__(self):
        self.USERS = {}
        # {username1: websocket1, username2: websocket2 .....}
        asyncio.run(self.create_server_and_ask())

    async def msgSender(self, msg):
        MainClass.sql.add_msg_json(msg)
        for k, v in self.USERS.items():
            await v.send(msg)

    async def handler(self, websocket):
        async for message in websocket:
            print("接收到" + str(message))
            data = json.loads(message)
            '''
                type: login logout send BotThinking BotReceived 
            '''
            if data["type"] == "login":  # 私发给他历史消息，然后广播他上线的消息。
                self.USERS[data["username"]] = websocket

                # 私发
                history_jsons = MainClass.sql.get_msg_json()
                for history_json in history_jsons:
                    # print("history_json: ", history_json)
                    await websocket.send(history_json[0])
                msg = {
                    "type": "notice",
                    "username": data["username"],
                    "content": '------以上为历史消息------',
                }
                await websocket.send(json.dumps(msg))
                # 广播
                msg = {
                    "type": "login",
                    "username": data["username"],
                    "content": '',
                }
                await self.msgSender(json.dumps(msg))
            elif data["type"] == "logout":
                msg = {
                    "type": "logout",
                    "username": data["username"],
                    "content": '',
                }
                self.USERS.pop(data["username"])
                # print(self.USERS)
                await self.msgSender(json.dumps(msg))
            elif data["type"] == "send":
                msg = {
                    "type": "send",
                    "username": data["username"],
                    "content": data["content"],
                }
                await self.msgSender(json.dumps(msg))
                if not MainClass.mychatbot.isThinking:
                    MainClass.mychatbot.isThinking = True
                    MainClass.mychatbot.question = data["content"]
                    msg2 = {
                        "type": "BotReceived",
                        "username": data["username"],
                        "content": ""
                    }
                else:
                    msg2 = {
                        "type": "BotThinking",
                        "username": "",
                        "content": ""
                    }
                await self.msgSender(json.dumps(msg2))

    async def create_server(self):
        serverip = "172.31.0.132"
        async with websockets.serve(self.handler, serverip, 1208):
            print("Server Booted")
            await asyncio.Future()  # run forever

    async def create_server_and_ask(self):
        task1 = asyncio.create_task(self.create_server())
        task2 = asyncio.create_task(MainClass.mychatbot.ask(self))
        await task1


if __name__ == "__main__":
    MainClass.sql = SQL()
    MainClass.mychatbot = MyChatBot()
    Server()
