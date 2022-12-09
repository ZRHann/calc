from revChatGPT.revChatGPT import Chatbot
import asyncio
import time
import websockets
import json
import threading
import re


class MainClass:
    mychatbot = None


class MyChatBot:
    def __init__(self):
        config = {
            # "email": "<YOUR_EMAIL>",
            # "password": "<YOUR_PASSWORD>"#,
            "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..dQXybc0XHnMJvQj4.B_nCE-mHm20fV2VCv-Jn8UFaXHZYRw9akU9uxyysHGL1Ne8m0kAcZ1XycYD6CHjznsyk3pIHf0N7g-HiS6Py--0h8JZBy9n-dzKaLPhwEOKRaQ3B98N_KmtSuI0HMqhmRpHNNlZyKdeXR2s5tH2Z86AyKnTB1GTcA6sphfHSEm424SMBqy8WZUWNT7HmEuQRMjvnpQRI2uo37ndF3pNGvyrSpXPhCeVpUwfc4b3U_WXiRSZi395MJXHEbdH-ZVk7MMeUkRl6pkZQv8U7BNT4i1nDVZSg9Co6hvyCeW0g1bQZ1C3FoKkrcxsMIes879NRuQTFu9kJMeDBmxyqQm4D3BdGSzVoEZYDpiDXDI1jJFBOY88KlV1_yyQU2cvPoMHEBVs7xMResmjFDtJmd1nsAAP_vUhI2KfRO7ubONiD-V9Z0X-FiEJU-vi5SNS2R4tAOwuxsMdiJlTsBY-8D-UjS2r7h9NCZEiGkjj2dv_ERCfISy37kuAlgwMOVmgAcNgTXH-W8LObcezF2_dtq1jcPhLjfA6Bmob8otZgMa8VqwRBa8JEDee32_QR7xzkVM9veLctiUgeArWUAOgbY05nzKuyh6NAFvDNX5WxEKbewyUPeyJ6zG7Qg-WwsO1Qo3TuM3bA4Pd2NP0NOb2nsZyOnToIMtBDRrsEPIdsnK0n06pT4oa3rLyo3jeAyWkG_V5Sb0hQSyTwkV4qRvOw8ODL1v_95j5lazl5R-EdE0i0uOrR8Gy9hHdfP2DqOmKsyYVqmVWJIBBAE3-LDufhGK02sIQn9UcVxN40E1AQ6HDU9gzZsXwGkeZZG9gpyuBSCMkTZ419fXzTyhLpt534tKcdvcmNbJst0AhZai8VwPNBw9lFYfhUu45EP2q4GPHfwi3nAX_ebJoWy9zuyimLdIPN1kmMI8m37EzOANYE1aZDxd5cOocv9Jh7fo5igKi5vOYcp4VtMJLdg8uxK7t305Ou70tpOol5MtD1hmmaHMcraMqAYiB7NUg3drOYlIwJIsVNusLKocptEZoF1G-u2ThLmhD2w79cgbrnnquydOfaCr35xysH4_sUJ2BvfJ9L6ylAgZndeI5BGj661_hVUHATgX2tMJqZHQrdrUMa3sY5CsqINjS7fGypyhOXIGlQtgcTR_XxviksmI4Q4Dl7ERsNqJiszAmLoU9pp7iwNjnEb2ZznFakbjfQlS3ve53SVP6--iiGBrpDtxpKfHztCZsbJ4Sb82PqwxxEO9dwYIZD0yGFqCZciSN1ybBwumeOVndfNlXIflk6d_5lst996HpfOjzDy9DyZa33fngA74UNCIL-DYW_wmwQfi2jnHcLUxXbUOhshkgs-9Y90PxClOW3DzvJzATDZgOnWWXy0v3jbANA8AzAI84O2eEzW5udtYcXIBOqSjFThcfy--drDJCol2f-XQQRq03y3ak0TReWm0uX857w5JQ0uQqCLeJcDKrg_ioanZgW5EvKdTZJDDyihgZeGpKovefyV0ZpbJtn5nO92GpIcm5FnW52dmSDkLkXrmY_nEqMhiOwjKuFyYwTRP_Jwwp0ytGGLJ4cTP5Xo90NdOvQEi20RjiIHPmJHeP4F8DD4gvL0eeUdd2LCYjAolZ3TBnzSCdV-YGom50BkVinWJjW_poTRSZa9DnMx0lMcK_4u_dhwioL6L6DFkUw8FOp5h00K61k_a1sh6ogtlDiPePke5O83hyPwq8zhTxOH9BwpVy3Kvea43CEwvlbSkz3m-oON54ZWuZJiK8-HIQ6NYJH7eYoyP067yUyppvutt3cxHJ2rz2IEDU4htqWkMvZNomhK7zMz7RmIU1Xe4Qkkvx2-aoCGlP-WfpamA28Tox0dC3SaJtHZ22sIFAmGa8WdPk0WaIA9LGvSVhTz5UEmQVUtL4ojtvCt__9n5gci9rOy8DXX3G8sLwmkPi3yXU2_Q9_WqcJGmKEdZWqgGp38UtRHaup946Oq_AOcXrN7mp7CiPx89mOERFuk80jm8tKEaiJPbnrA5vPvi9Vnumelu4w4Wmxz8D5Bse65ETj0a098HXSBbQO1kxMbRWdt4Rq_mRsXoq1DL52GMrOgYvXILNSAkjJ3z0_b-_jekjCNYPgzsFk69BDY3xFqOkZMz_AHdxd3Q4EUiLvTmolYJnfdc86O8f9nelV4NcpOXrxu9QDd-9QblEaiiBMvGpPhSQd8nb-CeBO-9Ze37VFhZH7kNGLREKeA9ifQ7m-i6Efxl8URYk.IG6KsOtss_P99lWrBZQBWg",
            # Deprecated. Use only if you encounter captcha with email/password
            # "proxy": "<HTTP/HTTPS_PROXY>"
        }
        self.isThinking = False
        self.chatbot = Chatbot(config, conversation_id=None)
        print("connected")

    async def ask(self, question, server1):
        print("Asked ChatGPT: ")
        print(question)
        response = self.chatbot.get_chat_response(question, output="text")
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
        asyncio.run(self.create_server())

    async def msgSender(self, msg):
        for k, v in self.USERS.items():
            await v.send(msg)

    async def handler(self, websocket):
        async for message in websocket:
            print("接收到" + str(message))
            data = json.loads(message)
            '''
                type: login logout send BotThinking BotReceived 
            '''
            if data["type"] == "login":
                self.USERS[data["username"]] = websocket
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
                    threading.Thread(target=MainClass.mychatbot.ask, args=(data["content"], self)).start()
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
        async with websockets.serve(self.handler, "172.31.0.132", 1208):
            print("Server Booted")
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    MainClass.mychatbot = MyChatBot()
    Server()

