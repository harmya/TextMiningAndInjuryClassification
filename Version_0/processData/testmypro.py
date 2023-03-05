import pandas as pd

df = pd.read_csv('../Data/AmazonReviews.csv')
text = list(df.body)

for t in text:
    print(t)
