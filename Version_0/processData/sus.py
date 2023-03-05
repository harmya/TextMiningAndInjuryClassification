import re

import pandas as pd

reddit = pd.read_csv("../Data/prediction_on_reddit_data.csv")
reddit['text'] = reddit['text'].astype('str')
reddit = reddit[reddit['label'] == 1]

lessened = []

for text in reddit.text:
    if 10 <= len(text.split(" ")) <= 25:
        text = re.sub(r'[^a-zA-Z ]+', ' ', text)
        text = re.sub(' +', ' ', text)
        lessened.append(text)


labels = []

for t in lessened:
    print(t)
    label = input()
    labels.append(label)


lessened_df = pd.DataFrame()
lessened_df['text'] = lessened
lessened_df.to_csv("lime_dataset.csv", index=False)

