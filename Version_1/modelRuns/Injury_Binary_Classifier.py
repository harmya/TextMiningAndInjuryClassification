import string
from collections import Counter

import nltk
import pandas as pd
from keras import layers
from keras.layers import Dropout
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from nltk.corpus import stopwords
from tensorflow import keras

df = pd.read_csv("model_dataset.csv")
print(df)

print((df.label == 0).sum())  # Non-Injury
print((df.label == 1).sum())  # Injury


def remove_punct(text):
    translator = str.maketrans("", "", string.punctuation)
    text = str(text)
    return text.translate(translator)


df["text"] = df.text.map(remove_punct)
print(df)

nltk.download('stopwords')
stop = set(stopwords.words("english"))


def remove_stopwords(text):
    filtered_words = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(filtered_words)


df["text"] = df.text.map(remove_stopwords)


def counter_word(text_col):
    count = Counter()
    for text in text_col.values:
        text = str(text)
        for word in text.split():
            count[word] += 1
    return count


counter = counter_word(df.text)
num_unique_words = len(counter)

train_size = int(df.shape[0] * 0.7)

train_df = df[:train_size]
val_df = df[train_size:]

# split text and labels
train_sentences = train_df.text.to_numpy()
train_labels = train_df.label.to_numpy()
val_sentences = val_df.text.to_numpy()
val_labels = val_df.label.to_numpy()

tokenizer = Tokenizer(num_words=num_unique_words)
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_sentences)
val_sequences = tokenizer.texts_to_sequences(val_sentences)

max_length = 32

train_padded = pad_sequences(train_sequences, maxlen=max_length, padding="post", truncating="post")
val_padded = pad_sequences(val_sequences, maxlen=max_length, padding="post", truncating="post")

reverse_word_index = dict([(idx, word) for (word, idx) in word_index.items()])


def decode(sequence):
    return " ".join([reverse_word_index.get(idx, "?") for idx in sequence])


decoded_text = decode(train_sequences[10])

model = keras.models.Sequential()
model.add(layers.Embedding(num_unique_words, 32, input_length=max_length))
model.add(layers.GRU(64, recurrent_dropout=0.4))
model.add(layers.Dense(1, activation="sigmoid", use_bias=True))

model.summary()

loss = keras.losses.BinaryCrossentropy(from_logits=False)
optim = keras.optimizers.Adam(lr=0.001)
metrics = ["accuracy"]

model.compile(loss=loss, optimizer=optim, metrics=metrics)

model.fit(train_padded, train_labels, epochs=2, validation_data=(val_padded, val_labels), verbose=2)

data = pd.read_csv('final_conclusion.csv', lineterminator='\n')
print(data)
data = data.dropna()
df_temp = data
data["text"] = data.text.map(remove_stopwords)

counter = counter_word(data.text)
num_unique_words = len(counter)

predict = data.text.to_numpy()
tokenizer.fit_on_texts(predict)
word_index = tokenizer.word_index

predict_seq = tokenizer.texts_to_sequences(predict)
predict_pad = pad_sequences(predict_seq, maxlen=max_length, padding="post", truncating="post")
predictions = model.predict(predict_pad)

for i in range(0, len(predictions)):
    if predictions[i] > 0.5:
        predictions[i] = 1
    else:
        predictions[i] = 0

print(predictions)
c = 0
for value in predictions:
    if value == 1:
        c += 1
print(c)
df_temp["label"] = predictions
data.to_csv('prediction_on_reddit_data(4).csv', index=False)
