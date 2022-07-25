# -*- coding: utf-8 -*-
"""task_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mrGAMntFDG9SUGzpk_TBxxCtpMYaS12e

Getting started with deepspeech
"""

!pip install deepspeech

"""We shall import necessary libraries"""

import librosa, librosa.display #used for music and audio analysis
import IPython.display as ipd #used to play audio files
import soundfile as sf 
import numpy as np
import pandas as pd


"""here we import model"""

!wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm #audio model
!wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer #deepspeech model

!ls

"""not sure what the curl command is exactly (similar to requests)"""

!curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz

!tar xvf audio-0.9.3.tar.gz
!ls -l ./audio/

"""checking the audio file

"""

y, s = librosa.load("audio/2830-3980-0043.wav", sr=16000)
ipd.Audio(y, rate=s)

!deepspeech --model deepspeech-0.9.3-models.pbmm --scorer deepspeech-0.9.3-models.scorer --audio audio/2830-3980-0043.wav > output.txt

data = pd.read_csv('output.txt', sep=" ", header=None)
data.to_csv('dataaa.csv', index = "content")

file1 = open("output.txt","r+") 
  
print("Output of Read function is ")
text_1 = file1.read()
print(text_1)

import gensim
from gensim.models import word2vec
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"

!ls -l

import gzip
import shutil
with gzip.open('GoogleNews-vectors-negative300.bin.gz', 'rb') as f_in:
    with open('GoogleNews-vectors-negative300.bin', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

#this still shows error
from gensim.models import KeyedVectors
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

"""there was an issue with loading the google news model, trying to build own model

"""

import gensim
import pandas as pd

!wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz

import gzip
import shutil
with gzip.open('reviews_Cell_Phones_and_Accessories_5.json.gz', 'rb') as f_in:
    with open('reviews_Cell_Phones_and_Accessories_5.json', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

df = pd.read_json('reviews_Cell_Phones_and_Accessories_5.json', lines = True)
df.head()

reviewtxt = df.reviewText.apply(gensim.utils.simple_preprocess)
#prepocessing the data

model = gensim.models.Word2Vec( window = 10, min_count =3, workers = 4 )
#initializing gensim model
#window id the target before and after given the word
#min_count refers to the no. of words in a sentence
#workers = no. of cpu cores

model.build_vocab(reviewtxt)

#model.epochs
#need to learn more about this
#model.corpus_count

model.train(reviewtxt, total_examples=model.corpus_count, epochs= model.epochs)

model.save("./word2vec-amazon-cell-accessories-review-short.model" )

print(data)
data.apply(model.wv.most_similar)

"""now will look into performing sentimental analysis on the obtained text

we will use vador( Valence Aware Dictionary for Sentiment Reasoning) for the sentiment reasoning
"""

import nltk 
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
sia.polarity_scores("experience proves this")

from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize 
txtt = sent_tokenize(text_1)
txt = word_tokenize(text_1)

tt = ["experience proves this"]
print(txtt)

ss = sia.polarity_scores(tt[0])
print(ss)

for sentence in tt:
  #bb=  sia.polarity_scores(sentence)
  print(sentence)
  ss = sia.polarity_scores(sentence)
  for k in sorted(ss):
    print('{0}: {1}, '.format(k, ss[k]), end='')
    print()

#bb

!pip install sentence_transformers

from sentence_transformers import SentenceTransformer
sentencess = ["experience proved it", "i am experienced", "this proves experience"]
model_ts = SentenceTransformer('all-mpnet-base-v2') #this converts the string to a dense vector space (768) which can then be used for similarity check
sentencess_embeddings = model_ts.encode(sentencess)
#output_embeddings = model_ts.encode(txtt)
output_embeddings = model_ts.encode("experience proves this")

!pip install sklearn
from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(output_embeddings, sentencess_embeddings[0:])

!pip install tensorflow
import tensorflow as tf
import tensorflow_hub as hub

sentencess = ["experience proved it", "i am experienced", "this proves experience"]
output = ["experience proves this"]
#model_ts = SentenceTransformer('all-mpnet-base-v2') #this converts the string to a dense vector space (768) which can then be used for similarity check
embed = hub.load("https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1")


sentencess_embeddings = embed(sentencess)
#output_embeddings = model_ts.encode(txtt)
output_embeddings = embed(output)

print(tf.keras.losses.cosine_similarity(output_embeddings, sentencess_embeddings[0:],axis =-1))

"""tensorflow pre trained model just uses 128 dimensional vector space so the accuracy is lesser compared to the hugging face model

now looking at converting audio files from different languages using google's resources
"""

!pip install SpeechRecognition

import speech_recognition as sr
r = sr.Recognizer()

with sr.AudioFile("/content/drive/MyDrive/AamirKhan_6.wav") as source:
  audio_text = r.listen(source)

  text = r.recognize_google(audio_text,language ="hi-IN")

print(text)

!pip install translators

import translators as ts
ts.google

ts._google.language_map
translation = ts.google(text, from_language='hi', to_language='en')
print(translation)
