# -*- coding: utf-8 -*-
"""Project_Code_G6_Part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CT7_RZwgeRwur47ILfAl7sY1FnYZH6Qr

## **NEWS ARTICLES TOPIC MODELING**
"""

import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding
import matplotlib.pyplot as plt

from google.colab import files
import pandas as pd

uploaded = files.upload()

df = pd.read_csv('fox.csv')

df[['text','label']].head()

sentiment_label = df.label.factorize()
sentiment_label # pos is 0, neg is 1

news = df.text.values

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(news)

encoded_docs = tokenizer.texts_to_sequences(news) # Replace the words with their assigned numbers using the text_to_sequence()

padded_sequence = pad_sequences(encoded_docs, maxlen=200)
padded_sequence # Use padding to pad the sentences to have equal length.

vocab_size = len(tokenizer.word_index) + 1
vocab_size

# Build the text classifier
embedding_vector_length = 32
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
model.add(SpatialDropout1D(0.5))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])
print(model.summary())

history = model.fit(padded_sequence,sentiment_label[0],validation_split=0.2, epochs=5, batch_size=32) # Train the model

plt.plot(history.history['accuracy'], label='acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.legend()
plt.ylim(0,1)
plt.show()

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.ylim(0,1)
plt.show()



import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')

data_text = df[['text']]
data_text['index'] = data_text.index
documents = data_text

def lemmatize_stemming(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

documents

doc_sample = documents[documents['index'] == 3534].values[0][0]
print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

processed_docs = documents['text'].map(preprocess)
processed_docs[:10]

dictionary = gensim.corpora.Dictionary(processed_docs)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[3534]

bow_doc_4310 = bow_corpus[3534]
for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0], 
                                               dictionary[bow_doc_4310[i][0]], 
bow_doc_4310[i][1]))

from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint
for doc in corpus_tfidf:
    pprint(doc)
    break

lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2) # Train the lda model using gensim.models.LdaMulticore

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic)) # Explore the words occurring in that topic and its relative weight

# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')

# Input text - to summarize
text = """(CNN)The Florida state Senate on Wednesday advanced legislation pushed by Republican Gov. Ron DeSantis during the state's special legislative session: a new congressional map submitted by the governor and a pair of bills aimed at Disney.

The DeSantis-backed map -- which proposes an aggressively partisan redrawing of the state's congressional boundaries that could help the Republican Party pick up four seats in the US House of Representatives this November -- passed the GOP-led Senate along party lines.
During the special session, state senators also passed a bill that would eliminate the unique status that allows Disney to operate as an independent government around its Orlando-area theme parks. One Republican, Sen. Jeff Brandes, voted with Democrats against the bill.
Additionally, the state Senate gave final passage along party lines to a bill that would eliminate a Disney carve-out in a social media bill that was signed into law last year but put on hold by a federal judge.
The Florida House still must pass the bills. It is expected to hold final debate and votes on Thursday.
The bills all have received blowback from Democrats in the state.
Democrats have criticized the map because it eliminates two seats held by Black members of Congress, while adding several likely Republican districts to the state.
The Republican-controlled legislature passed a different congressional district map during the regular session, but DeSantis vetoed that version. Florida Republicans then said they would allow the governor to decide how to reapportion the state's congressional districts. DeSantis offered his map last week, and it was the only version considered by the Senate during the special session.
While the special session was initially called to finalize the once-a-decade work of reapportioning congressional lines, state lawmakers added the Disney legislation to the docket after DeSantis on Tuesday escalated his weeks-long feud with Disney, challenging lawmakers in a surprise bombshell announcement to unravel the 55-year-old Reedy Creek Improvement Act, a unique Florida law that helped establish Walt Disney World in the state by giving the brains behind Mickey Mouse operational autonomy.
Within hours, Republican lawmakers delivered, advancing a pair of bills targeting Disney over its objections to a new law limiting classroom instruction on sexual orientation and gender identity.
"Once upon a time Disney was a great partner with the state of Florida," said Rep. Jackie Toledo, a Tampa Republican. "We've granted them privileges because of our shared history, shared goals and shared successes. Shamefully, Disney betrayed us."
It now appears almost certain that by the end of the week, the long-standing symbiotic arrangement that helped grow Disney into an iconic entertainment brand and Florida into an international travel destination could be dissolved.
GOP-controlled committees in the state House and Senate voted in favor of a bill that would end the special district on June 1, 2023.
Another bill, to subject Disney to a state law that allows people to sue Big Tech companies for censorship, also passed out of initial committees Tuesday afternoon. Disney had won an exemption from the bill last year. A federal judge has blocked the law but Florida is appealing the ruling.
Republicans in Florida and Disney have been at odds for months over legislation that prohibits schools from teaching young children about sexual orientation or gender identity. After initially declining to weigh in, Disney CEO Bob Chapek publicly criticized Florida lawmakers for passing what opponents called the "Don't Say Gay" bill and apologized to the company's LGBTQ employees for not being a stronger advocate.
Chapek announced that the company would stop making political donations in Florida after decades of contributing generously, mostly to Republicans, including a $50,000 donation to DeSantis' reelection effort."""

# Tokenizing the text
stopWords = set(stopwords.words("english"))
words = word_tokenize(text)

# Score of each word
freqTable = dict()
for word in words:
	word = word.lower()
	if word in stopWords:
		continue
	if word in freqTable:
		freqTable[word] += 1
	else:
		freqTable[word] = 1

# Calculate the score
sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
	for word, freq in freqTable.items():
		if word in sentence.lower():
			if sentence in sentenceValue:
				sentenceValue[sentence] += freq
			else:
				sentenceValue[sentence] = freq

sumValues = 0
for sentence in sentenceValue:
	sumValues += sentenceValue[sentence]

# Average value of a sentence from the original text

average = int(sumValues / len(sentenceValue))

# Storing sentences into our summary.
summary = ''
for sentence in sentences:
	if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.9 * average)):
		summary += " " + sentence
print(summary)