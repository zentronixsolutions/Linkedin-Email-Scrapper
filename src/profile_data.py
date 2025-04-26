import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
import json
from csv import writer
import pandas as pd

PATH = 'chromedriver-linux64/chromedriver'
AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
LINK = 'https://www.linkedin.com/'
LINK_FILE = 'client/client_links.csv'
DATA_FILE = 'client/client_data.csv'
COOKIES_FILE = 'client/client_cookies.json'


chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox") 
# chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f'user-agent={AGENT}')
chrome_options.add_argument("--window-size=811,616")

services = Service(PATH)
driver = webdriver.Chrome(service=services, options=chrome_options)

driver.get(LINK)
time.sleep(10)

with open(COOKIES_FILE, 'r') as file:
    cookies = json.load(file)
    
for cookie in cookies:
    driver.add_cookie(cookie)


df = pd.read_csv(LINK_FILE)
links = df['prfileUrls'].dropna().tolist()

for id, link in enumerate(links):
    data = []
    driver.get(f"{link}overlay/contact-info/")
    # time.sleep(5)
    data.append(id + 1)
    name = driver.find_elements(By.XPATH, "//h1[@id='pv-contact-info']")
    if name:
        data.append(name[0].text)
    else:
        data.append(None)
    email = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto')]")
    if email:
        data.append(email[0].text)
    else:
        data.append(None)
    data.append(link)
    print(data)
    with open(DATA_FILE, 'a', newline="",encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(data)