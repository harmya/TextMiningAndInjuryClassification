import praw as praw
import pandas as pd
i
client_id = 'mr1N30-RtWkrwHFIVwrcuQ'
client_secret = 'ansKPya9-TJl19H1Suz3EUjKzpMygw'
user_agent = 'DURI Research'
products = {
    'Electric Skateboard',
    'Electric Scooters',
    'Scooter',
    'Skateboard'
}
dict_values = dict()
injury_words = {
    'injury',
    'accident',
    'crashed',
    'crash',
}

reddit_obj = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

subreddit = reddit_obj.subreddit("all")
i = 0
data = []
query = "selftext:[skateboard injury]"
print(query)
for submission in subreddit.search(query, limit=None):
    if submission.is_self:
        text = submission.selftext
        words = text.split(" ")
        if len(words) > 5:
            data.append(text)
            i += 1
print(i)


'''
for product in products:
    for word in injury_words:
        query = "selftext:[skateboard injury]"
        print(query)
        for submission in subreddit.search(query, limit=None):
            if submission.is_self:
                text = submission.selftext
                words = text.split(" ")
                if len(words) > 5:
                    data.append(text)
                    i += 1
        print(i)
'''
data = set(data)
print(len(data))

dataframe = pd.DataFrame(data, columns=["text"])
dataframe.to_csv('redditPostsRUN.csv', index=False)

