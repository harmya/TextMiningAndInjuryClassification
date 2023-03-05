import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests

text_list = []
links = []
q = "https://www.reddit.com/search/?q=skateboard%20accident"
driver = webdriver.Chrome(executable_path="/Users/harmyabhatt/Downloads/chromedriver")

driver.get(f"{q}")
time.sleep(3)

prev = driver.execute_script("return document.body.scrollHeight")
i = 0

while True:
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(3)
    new = driver.execute_script("return document.body.scrollHeight")
    if i == 4:  # change number to get more data, this signifies the number of times the page will be scrolled till the end
        elements = driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            link = element.get_attribute("href")
            if link.__contains__("/comments"):
                links.append(link)
        break
    prev = new
    i += 1

print(len(links))
print(links)


narratives = []
text = []
for link in links:
    driver.get(link)
    post = driver.find_element(By.CSS_SELECTOR, "[data-test-id=post-content]")
    text = post.text.strip().split('\n')
    post_text = ""
    for t in text:
        if len(t.split(' ')) > 10:
            narratives.append(t)
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "[data-testid=comment]")
    for paragraph in paragraphs:
        data = paragraph.text
        narratives.append(data)

    print("GOO")
    time.sleep(5)

print(narratives)
print("Fin.")
df = pd.DataFrame()
df['text'] = narratives
df.to_csv('redditScrape.csv', index=False)
print(narratives)
