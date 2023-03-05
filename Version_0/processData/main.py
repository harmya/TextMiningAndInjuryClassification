import re

from bs4 import BeautifulSoup
import pandas as pd
import requests

path_to_neiss = "neiss_data.csv"
path_to_amazon = "../Data/AmazonReviews.csv"
path_to_posts = "redditPosts.csv"
path_to_comments = "../Data/redditCommentData.csv"

# pre-process neiss data and build neiss dataset
df_neiss = pd.read_csv(path_to_neiss)
final_neiss_set = []
for text in df_neiss.Narrative:
    text = str(text)  # convert to string
    text = text.lower()  # convert to lowercase
    cleanR = re.compile('<.*:-;>,')  # special characters
    cleantext = re.sub(cleanR, ' ', text)  # remove special characters
    rem_num = re.sub('[0-9]+', '', cleantext)  # remove numbers
    clear = rem_num.strip()  # remove white space
    clear = clear.replace("fx", ' ')
    clear = clear.replace('.', ' ')
    clear = clear.replace(',', ' ')
    clear = clear.replace(" l ", " left ")
    clear = clear.replace(" r ", " right ")
    clear = re.sub(' +', ' ', clear)
    clearText = clear.replace("dx", " ")  # remove the recurring "dx:" in neiss data
    finalText = clearText.split(" ", 1)[1]  # remove the recurring "yom" and "yof" markers
    final_neiss_set.append(str(finalText))

df_neiss_temp = pd.DataFrame(final_neiss_set, columns=["text"])
df_neiss_dataset = df_neiss_temp.sample(frac=1)  # randomly sampling a part of the entire dataset
df_neiss_dataset["label"] = 1  # labelling data as 1 = injury case
df_neiss_dataset.to_csv('neiss_dataset.csv', index=False)
print(len(df_neiss))

df_amazon = pd.read_csv(path_to_amazon)
final_amazon_list = []
for text in df_amazon.text:
    text = str(text)  # convert to string
    text = text.lower()  # convert to lowercase
    text = text.replace('\n', ' ')  # remove newlines
    cleanR = re.compile('<.*?>')  # special characters
    cleantext = re.sub(cleanR, '', text)  # remove special characters
    rem_num = re.sub('[0-9]+', '', cleantext)  # remove numbers
    clearText = rem_num.strip()  # remove white space
    final_amazon_list.append(str(clearText))

final_amazon_set = list(set(final_amazon_list))  # making sure the amazon dataset has no dupliates
df_amazon_dataset = pd.DataFrame(final_amazon_list, columns=["text"])
df_amazon_dataset["label"] = 0
df_amazon_dataset = df_amazon_dataset.sample(frac=0.9271)
print(len(df_amazon_dataset))
df_amazon_dataset.to_csv("amazon_dataset.csv", index=False)
'''
df_posts = pd.read_csv(path_to_posts)
df_comments = pd.read_csv(path_to_comments)
frames = [df_posts, df_comments]
df = pd.concat(frames)
reddit_list = []
for text in df.text:
    text = str(text)
    text = text.lower()  # convert to lowercase
    text = text.replace('{html}', "")  # remove html links
    text = text.replace('\n', ' ')  # remove newlines
    cleanr = re.compile('<.*?>')  # special chars
    cleantext = re.sub(cleanr, '', text)  # remove special cahrs
    rem_url = re.sub(r'http\S+', '', cleantext)  # remove hyperlinks
    rem_num = re.sub('[0-9]+', '', rem_url)  # remove words
    final_text = rem_num.strip()
    reddit_list.append(final_text)
    print(text)


df_temp = pd.DataFrame(reddit_list, columns=["text"])
df_reddit_dataset = df_temp.sample(frac=1)  # reducing the final set for easy human verification
df_reddit_dataset.to_csv("reddit_dataset.csv", index=False)
'''
df_neiss_dataset = pd.read_csv("neiss_dataset.csv")
frames = [df_neiss_dataset, df_amazon_dataset]
df = pd.concat(frames)
model_dataset = df.sample(frac=1)  # random shuffling of dataset
model_dataset = model_dataset.reset_index(drop=True)
model_dataset.to_csv("model_dataset.csv", index=False)
print(model_dataset)
