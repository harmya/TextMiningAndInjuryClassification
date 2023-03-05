# for text pre-processing
import re
import string
from IPython import display
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
# bag of words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
# for model-building
from sklearn.model_selection import train_test_split

# Read the data
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
df = pd.read_csv("../Data/model_dataset.csv")
df_train = df.sample(frac=0.08)
print(df_train.size)


# convert to lowercase, strip and remove punctuations
def preprocess(text):
    text = str(text)
    text = text.lower()
    text = text.strip()
    text = re.compile('<.*?>').sub('', text)
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = ' '.join([i for i in text.split() if i not in stopwords.words('english')])
    return text


# LEMMATIZATION
# Initialize the lemmatizer
wl = WordNetLemmatizer()


# function to map NTLK position tags
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# Tokenize the sentence
def lemmatizer(string):
    word_pos_tags = nltk.pos_tag(word_tokenize(string))  # Get position tags
    a = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for idx, tag in
         enumerate(word_pos_tags)]  # Map the position tag and lemmatize the word/token
    return " ".join(a)


def finalpreprocess(text):
    return lemmatizer(preprocess(text))


df_train['cleaned_text'] = df_train['text'].apply(lambda x: finalpreprocess(x))

# SPLITTING THE TRAINING DATASET INTO TRAINING AND VALIDATION
X_train, X_val, y_train, y_val = train_test_split(df_train["cleaned_text"], df_train["label"], test_size=0.2,
                                                  shuffle=True)

# TF-IDF
# Convert x_train to vector
tfidf_vectorizer = TfidfVectorizer(use_idf=True)
X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_val_vectors_tfidf = tfidf_vectorizer.transform(X_val)
# model
model = RandomForestClassifier(n_estimators=100, random_state=10)
model.fit(X_train_vectors_tfidf, y_train)
# Predict y value for test dataset
y_pred = model.predict(X_val_vectors_tfidf)
y_prob = model.predict_proba(X_val_vectors_tfidf)[:, 1]
print(classification_report(y_val, y_pred))
print('Confusion Matrix:', confusion_matrix(y_val, y_pred))

fpr, tpr, thresholds = roc_curve(y_val, y_prob)
roc_auc = auc(fpr, tpr)
print('AUC:', roc_auc)

from lime import lime_text
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline
from lime.lime_text import IndexedString, IndexedCharacters
from lime.lime_base import LimeBase
from sklearn.linear_model import Ridge, lars_path
from lime.lime_text import explanation
from functools import partial
import scipy as sp
from sklearn.utils import check_random_state

# Explaining the predictions and important features for predicting the label 1
c = make_pipeline(tfidf_vectorizer, model)
explainer = LimeTextExplainer(class_names=model.classes_)
# classifier_fn is the probability function that takes a string and returns prediction probabilities.
# num_features is the max. number of features we want in the explanation(default is 10).
# labels=(1,) means we want the explanation for the label 1
exp = explainer.explain_instance(X_val.iloc[20], c.predict_proba, num_features=5, labels=(1,))
exp.show_in_notebook().display()

## Perturbed samples are created in the neighbourhood of the instance of interest.
# classifier_fn is the probability function that takes a string and returns prediction probabilities.
# 5000 samples are created in the neighbourhood as default.
# Cosine distance is computed to calculate the distance between original and perturbed samples(default).

data, yss, distances = explainer._LimeTextExplainer__data_labels_distances(IndexedString(X_val.iloc[20]),
                                                                           classifier_fn=c.predict_proba,
                                                                           num_samples=5000)

## Top 2 closest perturbed samples
df = pd.DataFrame(distances, columns=['distance'])
df1 = df.sort_values(by='distance')
req_index = df1.index[1:3]
closest_perturbed_sample = []
for k in req_index:
    perturbed_text = ' '.join([re.split(r'\W+', X_val.iloc[20])[i] for i, x in enumerate(data[k]) if x == 1.0])
    closest_perturbed_sample.append(perturbed_text)
print(closest_perturbed_sample)


## Giving weightage to the perturbed samples
# Exponential kernel
def kernel(d, kernel_width):
    return np.sqrt(np.exp(-(d ** 2) / kernel_width ** 2))


# exponential kernel with kernel width 25
kernel_fn = partial(kernel, kernel_width=25)
# Samples weight using exponential kernel
weights = kernel_fn(distances)
