from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", '127.0.0.1:1208')
print("Start 1")
driver = webdriver.Chrome(options=options)

# 记得写完整的url 包括http和https
print("Start 2")
driver.get('https://chat.openai.com')
print(driver.page_source)
# 程序打开网页后120秒内 “手动登陆账户”
WebDriverWait(driver, 1000).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/button'))
)

with open('cookies.txt', 'w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))

driver.close()
