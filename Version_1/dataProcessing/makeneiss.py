import pandas as pd
import csv
import re
import ast
import string

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U0001F1F2-\U0001F1F4"  # Macau flag
                           u"\U0001F1E6-\U0001F1FF"  # flags
                           u"\U0001F600-\U0001F64F"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U0001F1F2"
                           u"\U0001F1F4"
                           u"\U0001F620"
                           u"\u200d"
                           u"\u2640-\u2642"
                           "]+", flags=re.UNICODE)

'''
df_2019 = pd.read_csv('NEISS_2019.csv')
df_2020 = pd.read_csv('NEISS_2020.csv')
df_2021 = pd.read_csv('NEISS_2021.csv')
df_2018 = pd.read_csv('NEISS_2018.csv')
col = ['CPSC_Case_Number',
       'Treatment_Date',
       'Age',
       'Sex',
       'Race',
       'Other_Race',
       'Hispanic',
       'Other_Diagnosis',
       'Other_Diagnosis_2',
       'Disposition',
       'Location',
       'Fire_Involvement',
       'Alcohol',
       'Drug',
       'Product_1',
       'Product_2',
       'Product_3',
       'Stratum',
       'PSU',
       'Weight']

df_2018 = df_2018.drop(columns=col)
df_2019 = df_2019.drop(columns=col)
df_2020 = df_2020.drop(columns=col)
df_2021 = df_2021.drop(columns=col)


frames = [df_2018, df_2019, df_2021, df_2020]
df = pd.concat(frames)
df = df.reset_index(drop=True)
df.to_csv('neiss_data.csv', index=False)
'''
ok = 'Äô'
df_s = pd.read_csv('redditFinalScrape.csv', lineterminator='\n')
df_r = pd.read_csv('reddit_dataset.csv', lineterminator='\n')

n = []

for text in df_s.text:
    text = str(text)
    text = text.replace(ok, '')
    words = text.split(' ')
    if len(words) > 5:
        n.append(text)

for text in df_r.text:
    text = str(text)
    text = text.replace(ok, '')
    words = text.split(' ')
    if len(words) > 20:
        n.append(text)

narratives = list(set(n))
print(len(narratives))

text_data = []
for text in narratives:
    text = str(text)
    text = text.lower()  # convert to lowercase
    text = text.replace('{html}', "")  # remove html links
    text = text.replace('\n', ' ')  # remove newlines
    cleanr = re.compile('<.*?:;>')  # special chars
    cleantext = re.sub(cleanr, ' ', text)  # remove special chars
    rem_url = re.sub(r'http\S+', '', cleantext)  # remove hyperlinks
    rem_num = re.sub('[0-9]+', '', rem_url)  # remove words
    final_text = rem_num.strip()
    final_text = re.sub(' +', ' ', final_text)
    final_text = re.sub('\n+', ' ', final_text)
    final_text = emoji_pattern.sub(r'', final_text)
    final_text = final_text.replace('Äô', '')
    final_text = final_text.replace('Ä¶', '')
    final_text = final_text.replace('Äù', '')
    final_text = final_text.replace('Äì', '')
    final_text = final_text.replace('Ä', '')
    final_text = final_text.replace(',', '')
    words = final_text.split(' ')
    
    text_data.append(final_text.strip())


def remove_punct(t):
    translator = str.maketrans("", "", string.punctuation)
    t = str(t)
    return t.translate(translator)


for val in text_data:
    if val == ' ':
        text_data.remove(val)


df = pd.DataFrame(text_data, columns=['text'])
df["text"] = df.text.map(remove_punct)
df = df.dropna()
df = df.sample(frac=0.8)
df.to_csv('reddit_prediction_dataset.csv', index=False)
print(df)

