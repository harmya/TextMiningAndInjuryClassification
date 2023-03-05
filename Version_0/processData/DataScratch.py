import pandas as pd

#df1 = pd.read_csv('Data/1429_1.csv')
#df2 = pd.read_csv('Data/neiss.csv')

df3 = pd.read_csv('eskate_neiss.csv')
data = []
i = 0
for text in df3.text:
    words = text.split(' ')
    if len(words) > 35:
        data.append(text)
        i += 1



'''
data = []
for text in df2.text:
    words = text.split(' ')
    if len(words) > 35:
        data.append(text)

print(len(data))

df3 = pd.DataFrame(data, columns=['text'])

df1['label'] = 0
df3['label'] = 1

frames = [df1, df3]

df = pd.concat(frames)
shuffled = df.sample(frac=1)

shuffled = shuffled[500:1500]

shuffled.to_csv('Data/NarrativeDataset.csv', index=False)
'''