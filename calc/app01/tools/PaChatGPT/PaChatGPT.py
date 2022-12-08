import os

os.chdir('../../../')
print('当前工作目录', os.getcwd())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument('enable-automation')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('enable-features=NetworkServiceInProcess')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://chat.openai.com/chat")

print(driver.page_source)

time.sleep(3)
WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[4]/button[1]'))
)
btn2 = driver.find_element('xpath', '/html/body/div/div/div/div[4]/button[1]')
btn2.click()
print("btn2 clicked")

WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/div/div/div/form/div[1]/div/div[1]/div/input'))
)
textarea2 = driver.find_element('xpath', '/html/body/main/section/div/div/div/form/div[1]/div/div[1]/div/input')
btn4 = driver.find_element('xpath', '/html/body/main/section/div/div/div/form/div[2]/button')
textarea2.send_keys("2829442630@qq.com")
btn4.click()


WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
)
textarea3 = driver.find_element('xpath', '//*[@id="password"]')
btn3 = driver.find_element('xpath', '/html/body/main/section/div/div/div/form/div[2]/button')
textarea3.send_keys("zg801zrh160118.")
btn3.click()

WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button'))
)
btn5 = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button')
btn5.click()

WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]'))
)
btn6 = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
btn6.click()

WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]'))
)
btn7 = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]')
btn7.click()




WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button'))
)
textarea1 = driver.find_element("xpath", '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/textarea')
btn1 = driver.find_element("xpath", '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button')



def SendAndReceive(msg):
    textarea1.send_keys(msg)
    btn1.click()
    WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button'))
    )
    BotAnswerP = driver.find_elements("xpath", '/html//p')[-2]
    print(BotAnswerP.text)


def GetLoginCookie():
    cookie = ""
    with open('cookies.txt', 'r') as f:
        cookie = f.read()
    print(cookie)


SendAndReceive("3543")
SendAndReceive("hello")

driver.close()
