import pandas as pd

df = pd.read_csv('AmazonReviews.csv')
text = list(df.body)

for t in text:
    print(t)
