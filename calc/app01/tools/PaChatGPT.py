import os
os.chdir('../../')
print('当前工作目录', os.getcwd())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

option = webdriver.FirefoxOptions()

profile_dir = r'./app01/MyData/a2s3528m.default-release'
conf_profile = webdriver.FirefoxProfile(profile_dir)
driver = webdriver.Firefox(conf_profile)
driver.get("https://chat.openai.com/")


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


SendAndReceive("3543")
SendAndReceive("hello")


driver.close()
