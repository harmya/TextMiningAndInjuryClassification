import time

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
text_list = []


products = ["Electric%20Skateboard", "Electric%20Scooter", "Skateboard",
            "Scooter"]  # use %20 instead of space when writing a query
keywords = ["injury", "accident", "crash"]

q = "https://www.reddit.com/search/?q=selftext%3A%5Bskateboard%20injury%5D"
driver = webdriver.Chrome(executable_path="/Users/harmyabhatt/Downloads/chromedriver")
for product in products:
    for keyword in keywords:
        driver.get(f"{q}")
        time.sleep(3)
        element = driver.find_element(by="data-click-id=")
        print(element)
        prev = driver.execute_script("return document.body.scrollHeight")
        i = 0
        while True:
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(3)
            new = driver.execute_script("return document.body.scrollHeight")

            if i == 5:  # change number to get more data, this signifies the number of times the page will be scrolled till the end
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                ok = soup.find_all('p')
                for comment in ok:
                    comment_text = comment.text
                    if not comment_text.__contains__("https://"):
                        comment_original = comment_text.split(">")
                        text_list.append(comment_original[0])
                break

            prev = new
            i += 1

text_list = set(text_list)
print(len(text_list))
text_list = list(text_list)
df = pd.DataFrame()
df['text'] = text_list
df.to_csv('redditCommentData.csv', index=False)
