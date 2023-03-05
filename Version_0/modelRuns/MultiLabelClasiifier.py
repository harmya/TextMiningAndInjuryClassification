import ast
import re

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier

df_multi = pd.read_csv("neiss_data.csv")

df_multi["Diagnosis_2"] = df_multi["Diagnosis_2"].astype("Int64")
df_multi = df_multi.fillna(-1)
df_multi["Diagnosis"] = df_multi["Diagnosis"].astype("Int64")
df_multi = df_multi.fillna(-1)

list_1 = df_multi["Diagnosis"]
list_2 = df_multi["Diagnosis_2"]

neiss_set = []
for text in df_multi.Narrative:
    text = str(text)  # convert to string
    text = text.lower()  # convert to lowercase
    cleanR = re.compile('<.*:-;>,')  # special characters
    cleantext = re.sub(cleanR, ' ', text)  # remove special characters
    rem_num = re.sub('[0-9]+', ' ', cleantext)  # remove numbers
    clear = rem_num.strip()  # remove white space
    clear = clear.replace("fx", ' ')
    clear = clear.replace('.', ' ')
    clear = clear.replace(',', ' ')
    clear = clear.replace(" l ", " left ")
    clear = clear.replace(" r ", " right ")
    clear = re.sub(' +', ' ', clear)
    clearText = clear.replace("dx", " ")  # remove the recurring "dx:" in neiss data
    finalText = clearText.split(" ", 1)[1]  # remove the recurring "yom" and "yof" markers
    neiss_set.append(str(finalText))

df_multi = pd.DataFrame()
df_multi['text'] = neiss_set
list_final = []
for i in range(0, len(list_2)):
    if list_2[i] == -1:
        text = '[\'' + list_1[i].astype(str) + '\']'
        list_final.append(text)
    else:
        text = '[\'' + list_1[i].astype(str) + '\', \'' + list_2[i].astype(str) + '\']'
        list_final.append(text)

df_multi['label'] = list_final

df_multi['label'] = df_multi['label'].apply(lambda evaluate: ast.literal_eval(evaluate))

print(df_multi)

multilabel = MultiLabelBinarizer()
y = df_multi['label']
y = multilabel.fit_transform(df_multi['label'])
print("y is")
print(y)
print(multilabel.classes_)

df_n = pd.DataFrame(y, columns=multilabel.classes_)

tfidf = TfidfVectorizer(analyzer='char_wb', max_features=50000, ngram_range=(1, 2))
X = tfidf.fit_transform(df_multi['text'])


x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)

svc = LinearSVC()
sgd = SGDClassifier()
lr = LogisticRegression(solver='lbfgs')

classifier = sgd


clf = OneVsRestClassifier(classifier)

clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

x = pd.read_csv('final_conclusion.csv', index_col=False)
dataset = []
for i in range(0, x.count()[0]):
    if x.iloc[i][2] == 1:
        dataset.append(x.iloc[i][0])


xt = tfidf.transform(dataset)
clf.predict(xt)
labels = multilabel.inverse_transform(clf.predict(xt))

predictions = pd.DataFrame(dataset, columns=["text"])
predictions["label"] = labels
print(predictions)
predictions.to_csv('DiagnosisDiya.csv', index=False)

import os

df_results = pd.read_csv('DiagnosisDiya.csv')
df_results['label'] = df_results['label'].apply(lambda evaluate: ast.literal_eval(evaluate))
text = []
labels = []
for i in range(0, df_results.count()[0]):
    label = df_results.iloc[i][1]
    if label:
        text.append(df_results.iloc[i][0])
        labels.append(label)

body_codes = {
    33: "Arm, lower (not including elbow or wrist)",
    80: "Arm, upper",
    37: "Ankle",
    94: "Ear",
    32: "Elbow",
    77: "Eyeball",
    76: "Face (including eyelid, eye area and nose)",
    92: "Finger",
    83: "Foot",
    82: "Hand",
    75: "Head",
    0: "Internal (use with aspiration and ingestion)",
    35: "Knee",
    36: "Leg, lower (not including knee or ankle)",
    81: "Leg, upper",
    88: "Mouth (including lips, tongue and teeth)",
    89: "Neck",
    38: "Pubic region",
    30: "Shoulder (including clavicle, collarbone)",
    93: "Toe",
    79: "Trunk, lower",
    31: "Trunk, upper (not including shoulders)",
    34: "Wrist",
    84: "25-50% of body (used for burns only)",
    85: "All parts of body (more than 50% of body)",
    87: "Not recorded"
}
diagnoses_codes = {
    41: 'INGESTION',
    42: 'ASPIRATION',
    46: 'BURN, ELECTRICAL',
    47: 'BURN, NOT SPEC.',
    48: 'BURN, SCALD',
    49: 'BURN, CHEMICAL',
    50: 'AMPUTATION',
    51: 'BURNS, THERMAL',
    52: 'CONCUSSION',
    53: 'CONTUSIONS, ABR.',
    54: 'CRUSHING',
    55: 'DISLOCATION',
    56: 'FOREIGN BODY',
    57: 'FRACTURE',
    58: 'HEMATOMA',
    59: 'LACERATION',
    60: 'DENTAL INJURY',
    61: 'NERVE DAMAGE',
    62: 'INTERNAL INJURY',
    63: 'PUNCTURE',
    64: 'STRAIN, SPRAIN',
    65: 'ANOXIA',
    66: 'HEMORRHAGE',
    67: 'ELECTRIC SHOCK',
    68: 'POISONING',
    69: 'SUBMERSION',
    70: 'OTHER',
    71: 'OTHER',
    72: 'AVULSION',
    73: 'RADIATION',
    74: 'DERMA/CONJUNCT',
    0: 'NO INJURY',
    1: 'TREATED/EXAMINED AND RELEASED',
    2: 'TREATED AND TRANSFERRED',
    4: 'TREATED AND ADMITTED/HOSPITALIZED',
    5: 'HELD FOR OBSERVATION',
    6: 'LEFT WITHOUT BEING SEEN',
    8: 'FATALITY INCL. DOA, DIED IN ER',
    9: 'UNKNOWN, NOT STATED'
}

df_results_multi = pd.DataFrame(text, columns=['text'])
df_results_multi['label'] = labels
body_part = []
for item in labels:
    part = []
    for value in item:
        part.append(diagnoses_codes.get(int(value)))
    body_part.append(part)

df_results_multi['body_part'] = body_part
print(df_results_multi)
df_results_multi.to_csv('multilabel-prediction-diagnosis.csv', index=False)
