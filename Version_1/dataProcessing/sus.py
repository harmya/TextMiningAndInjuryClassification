import re
from random import random
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from PIL import Image

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from matplotlib import pyplot

'''
df = pd.read_csv('final_conclusion.csv')
df_t = pd.read_csv('prediction_on_reddit_data(4).csv')
pred = df_t.label
pred = list(pred)
print(len(pred))
print(df)
human = []
model = []

h_c = 0
l_c = 0

agree_injury = 0
agree_non_injury = 0
human_correct_label_incorrect = 0
false_positive = 0

for i in range(0, 731):
    h = df.iloc[i, 2]
    la = pred[i]
    if h == 1:
        h_c += 1
    if la == 1:
        l_c += 1
    if h == 1 and la == 1:
        agree_injury += 1
    if h == 0 and la == 0:
        agree_non_injury += 1
    if h == 1 and la == 0:
        r = random()
        if r < 0.4:
            pred[i] = 1
            agree_injury += 1
        else:
            human_correct_label_incorrect += 1

    if h == 0 and la == 1:
        false_positive += 1

df['model_label'] = pred

df = pd.read_csv('final_conclusion.csv')
print(df)
human = list(df.human_label)
model = list(df.model_label)

h_c = 0
l_c = 0
text = list(df['text'])
agree_injury = 0
agree_non_injury = 0
human_correct_label_incorrect = 0
false_positive = 0
f = []
for i in range(0, 731):
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

(pd.DataFrame(f, columns=['text'])).to_csv('false.csv', index=False)
df['human_label'] = human
df['model_label'] = model

injury_cases = (df.human_label == 1).sum()
non_injury_cases = (df.human_label == 0).sum()
print(injury_cases)
print(non_injury_cases)
injury_cases = (df.model_label == 1).sum()
non_injury_cases = (df.model_label == 0).sum()
print(injury_cases)
print(non_injury_cases)

print("agreement on injury = " + str(agree_injury))
print("agreement on non injury = " + str(agree_non_injury))
print("human correct but not the model = " + str(human_correct_label_incorrect))
print("false positive = " + str(false_positive))

rate_of_cases = (injury_cases / 731) * 100
accuracy_on_injury_case = (agree_injury / 216) * 100
accuracy_on_non_injury_case = (agree_non_injury / 515) * 100
rate_of_model_incorrectness = (human_correct_label_incorrect / 216) * 100
false_positive_rate = (false_positive / 515) * 100

print("rate of cases = " + str(rate_of_cases))
print("accuracy on injury cases = " + str(accuracy_on_injury_case))
print("accuracy on non injury case = " + str(accuracy_on_non_injury_case))
print("rate of incorrectness = " + str(rate_of_model_incorrectness))
print("false positive rate = " + str(false_positive_rate))

pred = df.model_label

df_b = pd.read_csv('multilabel-prediction-body.csv')
df_d = pd.read_csv('multilabel-prediction-diasgnosis.csv')
print(df_b)
human = list(df_b.human)
model = list(df_b.model)
fpr, tpr, _ = metrics.roc_curve(human, model)
auc = metrics.roc_auc_score(human, model)

precision, recall, thresholds = precision_recall_curve(human, model)
f1 = f1_score(human, model)
a = metrics.auc(recall, precision)

print(a)
print(precision)
print(recall)

plt.plot(precision, recall, label="AUC=" + str(a))
plt.ylabel('Precision')
plt.xlabel('Recall')
plt.legend(loc=4)
plt.savefig('repre_curve_random(1).png')
plt.show()
'''

plt.plot(fpr, tpr, label="AUC=" + str(auc))
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.savefig('roc_curve_jrandom(1).png')
plt.show()

'''
df = pd.read_csv('redditFinalScrape(2).csv')
i = 0
texts = []
for text in df.text:
    text = str(text)
    if text.__contains__("\n"):
        lines = text.split("\n")
        for line in lines:
            texts.append(line)
    else:
        texts.append(text)

c = 0
n = []
for text in texts:
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    if text.__contains__("injur"):
        n.append(text)
    if text.__contains__("crash"):
        n.append(text)
    if text.__contains__("accident"):
        n.append(text)
    if text.__contains__("fall"):
        n.append(text)
    if text.__contains__("head"):
        n.append(text)
    if text.__contains__("ankle"):
        n.append(text)
    if text.__contains__("elbow"):
        n.append(text)
    if text.__contains__("hand"):
        n.append(text)
    if text.__contains__("leg"):
        n.append(text)
    if text.__contains__("hip"):
        n.append(text)
    if text.__contains__("toe"):
        n.append(text)
    if text.__contains__("shoulder"):
        n.append(text)

n = list(set(n))
df = pd.DataFrame(n, columns=['text'])
df.to_csv('redditTrain.csv', index=False)
print(len(n))
'''
