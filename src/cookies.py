import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
import json

PATH = 'chromedriver-win64/chromedriver.exe'
AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
LINK = 'https://www.linkedin.com/'
FILE_NAME = 'client_cookies.json'

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={AGENT}')

services = Service(PATH)
driver = webdriver.Chrome(service=services, options=chrome_options)

driver.get(LINK)
time.sleep(300)

cookie = driver.get_cookies()

with open(FILE_NAME, 'w') as file:
    json.dump(cookie, file)

print("Done")