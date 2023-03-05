import pandas as pd
from IPython.display import display
import random
'''
df_diya = pd.read_csv('DiagnosisDiya.csv')

df = pd.read_csv('multilabel-prediction-body.csv')
display(df)
body = set(list(df.text))
body_labels = []
d_labels = []
for text in df_diya.text:
    if body.__contains__(text):
        body_labels.append(1)
    else:
        body_labels.append(0)
for text in df_diya.label:
    if text == '()':
        d_labels.append(0)
    else:
        d_labels.append(1)

print(len(body_labels))
df_diya['body_labels'] = body_labels
df_diya['diag_labels'] = d_labels
df_diya.to_csv('multifuckok.csv', index=False)
display(df_diya)
'''
df = pd.read_csv('okyarbruh.csv')
body = []
diag = []
model = list(df.body_labels)
human = list(df.body)


h_c = 0
l_c = 0
text = list(df['text'])
agree_injury = 0
agree_non_injury = 0
human_correct_label_incorrect = 0
false_positive = 0
f = []
for i in range(0, 216):
    h = human[i]
    la = model[i]
    if h == 1:
        h_c += 1
    if la == 1:
        l_c += 1
    if h == 1 and la == 1:
        agree_injury += 1
    if h == 0 and la == 0:
        agree_non_injury += 1
    if h == 1 and la == 0:
        human_correct_label_incorrect += 1
    if h == 0 and la == 1:
        f.append(text[i])
        false_positive += 1

print(agree_injury)
print(agree_non_injury)
print(human_correct_label_incorrect)
print(false_positive)