import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
import json
from csv import writer
import pandas as pd
import os

PATH = 'chromedriver-win64/chromedriver.exe'
AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
LINK = 'https://www.linkedin.com/'
FILE_NAME = 'test_links.csv'
COOKIES_FILE = 'client_cookies.json'
batch = 0


chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox") 
# chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f'user-agent={AGENT}')
chrome_options.add_argument("--window-size=811,616")

services = Service(PATH)
driver = webdriver.Chrome(service=services, options=chrome_options)

driver.set_script_timeout(60)
driver.get(LINK)
time.sleep(10)

with open(COOKIES_FILE, 'r') as file:
    cookies = json.load(file)
    
for cookie in cookies:
    driver.add_cookie(cookie)
    
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
time.sleep(10)

# Scroll down to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    driver.execute_script(f"window.scrollTo(document.body.scrollHeight, {last_height - 2000});")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    
    elements = driver.find_elements(By.XPATH, "//div[@class='scaffold-finite-scroll__content']//li//div[@class='mn-connection-card__details']//a")  
        
    batch_ = elements[batch:]
    batch_links = driver.execute_script("return Array.from(arguments[0], e => e.href);", batch_)
    batch = len(elements)
    
    with open(FILE_NAME, 'a', newline='', encoding='utf-8') as file:
        writers = writer(file)
        link = [[i] for i in batch_links]
        writers.writerows(link)
        file.close()

    # Calculate new scroll height and compare with last scroll height

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:       
        break
    
    last_height = new_height


driver.quit()
print("Done")