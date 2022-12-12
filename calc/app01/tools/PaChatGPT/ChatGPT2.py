import traceback

from revChatGPT.revChatGPT import AsyncChatbot as Chatbot
import asyncio
import time
import websockets
import json
import threading
import re
import pymysql
import random
import string


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
            try:
                self.db.rollback()
            except:
                pass
            finally:
                print("Failed to Add a msg_json to database: ")
                traceback.print_exc()  # 打印异常信息

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
            traceback.print_exc()  # 打印异常信息
            return []


class MyChatBot:
    def __init__(self):
        config = {
            # "email": "2829442630@qq.com",
            # "password": "zg801zrh160118.",
            # Deprecated. Use only if you encounter captcha with email/password
            # "proxy": "<HTTP/HTTPS_PROXY>"
            "session_token": "",
            "cf_clearance": "",
            "user_agent": "",
        }
        with open("session_token.txt", "r") as f:
            config["session_token"] = f.read()
        with open("cf_clearance.txt", "r") as f:
            config["cf_clearance"] = f.read()
        with open("user_agent.txt", "r") as f:
            config["user_agent"] = f.read()
        self.isThinking = False
        try:
            self.chatbot = Chatbot(config, conversation_id=None)
            print("connected")
        except Exception as ex:
            traceback.print_exc()
        self.question = ""

    async def ask(self, server1):
        while True:
            await asyncio.sleep(0.3)
            if self.isThinking:
                print("Asked ChatGPT: ")
                print(self.question)
                msg1 = {}
                answer_id = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                try:
                    response = await self.chatbot.get_chat_response(self.question, output="stream")
                    async for res in response:
                        await asyncio.sleep(0.03)
                        print("ChatGPT answered: ", res["message"])
                        msg1 = {
                            "type": "BotAnswer",
                            "username": "ChatGPT",
                            "content": res["message"],
                            "answer_id": answer_id,
                        }
                        await server1.msgSender(json.dumps(msg1))
                except Exception as ex:
                    print("ChatGPT Failed To Answer")
                    traceback.print_exc()
                    msg1 = {
                        "type": "BotAnswerFailed",
                        "username": "ChatGPT",
                        "content": "",
                        "answer_id": answer_id,
                    }
                    await server1.msgSender(json.dumps(msg1))
                finally:
                    self.isThinking = False



class Server:
    def __init__(self):
        self.USERS = {}
        # {username1: websocket1, username2: websocket2 .....}
        asyncio.run(self.create_server_and_ask())

    async def msgSender(self, msg):
        MainClass.sql.add_msg_json(msg)
        for k, v in self.USERS.items():
            try:
                await v.send(msg)
            except Exception as ex:
                traceback.print_exc()

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
        await task2


if __name__ == "__main__":
    MainClass.sql = SQL()
    MainClass.mychatbot = MyChatBot()
    Server()
