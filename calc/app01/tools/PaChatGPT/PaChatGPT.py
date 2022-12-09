import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import time
import websockets
import json
import re
import base64
import uuid
os.chdir('../../../')
print('当前工作目录', os.getcwd())


class Pa:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('enable-features=NetworkServiceInProcess')
        chrome_options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://chat.openai.com/chat")
        print(self.driver.page_source)

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[4]/button[1]'))
        )
        btn2 = self.driver.find_element('xpath', '/html/body/div/div/div/div[4]/button[1]')
        btn2.click()
        print("btn2 clicked")

        while "error" in self.driver.title or \
                len(self.driver.find_elements('xpath', '//*[@id="username"]')) == 0:
            btn2 = self.driver.find_elements('xpath', '/html/body/div/div/div/div[4]/button[1]')
            if len(btn2) > 0:
                btn2[0].click()
            time.sleep(0.5)

        print("located to the email input page")
        textarea2 = self.driver.find_element('xpath', '//*[@id="username"]')
        textarea3 = self.driver.find_elements('xpath', '//*[@id="captcha"]')
        btn4 = self.driver.find_element('xpath', '/html/body/main/section/div/div/div/form/div[2]/button')
        img1 = self.driver.find_elements('xpath',
                                        '/html/body/main/section/div/div/div/form/div[1]/div/div[2]/div[1]/img')
        textarea2.send_keys("2829442")
        time.sleep(0.1)
        textarea2.send_keys("630@qq.com")
        time.sleep(0.1)
        if len(img1) > 0:
            print("Found Verification Code.")
            self.ParseVerCode(img1[0].get_attribute('src'))
            ver_code = input()
            textarea3[0].send_keys(ver_code)
            time.sleep(0.1)
        btn4.click()
        print("email entered, Verification code entered, btn4 clicked")

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
        )
        textarea3 = self.driver.find_element('xpath', '//*[@id="password"]')
        btn3 = self.driver.find_element('xpath', '/html/body/main/section/div/div/div/form/div[2]/button')
        textarea3.send_keys("zg801zr")
        time.sleep(0.1)
        textarea3.send_keys("h160118.")
        time.sleep(0.1)
        btn3.click()
        print("password entered, btn3 clicked")

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button'))
        )
        btn5 = self.driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button')
        btn5.click()

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]'))
        )
        btn6 = self.driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
        btn6.click()

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]'))
        )
        btn7 = self.driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
        btn7.click()

        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button'))
        )
        self.HumanInputArea = self.driver.find_element("xpath",
                                                       '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/textarea')
        self.HumanInputBtn = self.driver.find_element("xpath",
                                                      '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button')

    def SendAndReceive(self, msg):
        self.HumanInputArea.send_keys(msg)
        self.HumanInputBtn.click()
        print("Sended To ChatGPT: ", msg)
        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button'))
        )
        BotAnswerP = self.driver.find_elements("xpath", '/html//p')[-2]
        print("Received From ChatGPT: ", BotAnswerP.text)
        return BotAnswerP.text

    def ParseVerCode(self, src):
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")

        else:
            raise Exception("Verification Code Do not parse!")
        # 2、base64解码
        img = base64.urlsafe_b64decode(data)

        # 3、二进制文件保存
        filename = "./app01/tools/PaChatGPT/VerificationCode.{}".format(ext)
        with open(filename, "wb") as f:
            f.write(img)
        print("Verification Code Parsed and Saved Successfully")


class Server:
    def __init__(self):
        self.USERS = {}
        # {username1: websocket1, username2: websocket2 .....}
        self.create_server()

    async def msgSender(self, msg):
        for k, v in self.USERS.items():
            await v.send(msg)

    async def handler(self, websocket):
        async for message in websocket:
            print("接收到" + str(message))
            data = json.loads(message)
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
                print(self.USERS)
                await self.msgSender(json.dumps(msg))
            elif data["type"] == "send":
                msg = {
                    "type": "send",
                    "username": data["username"],
                    "content": data["content"],
                }
                await self.msgSender(json.dumps(msg))

    async def create_server(self):
        async with websockets.serve(self.handler, "172.31.0.132", 9999):
            print("Server Booted")
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    pa = Pa()
    # server = Server()

    pa.SendAndReceive("3543")
    pa.SendAndReceive("hello")

    pa.driver.close()
