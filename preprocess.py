from lxml import etree
import re
import json
import os
import sqlite3
#import lda
#from sklearn.feature_extraction.text import CountVectorizer
import itertools
import pandas as pd
import gensim
import nltk
import nltk.tokenize
from nltk.tokenize import MWETokenizer



conn = sqlite3.connect('rechtspraak.db')
c = conn.cursor()


#stemmer = nltk.stem.snowball.DutchStemmer(ignore_stopwords=True)
def tokenize(text):
    tokenized = nltk.word_tokenize(text)
    #return [stemmer.stem(w) for w in tokenized if w.isalnum()]
    #tokenizeMulti = MWETokenizer([('artikel', '6')])       #Kan dit met regex?
    #print(tokenized)
    #tokenized2 = tokenizeMulti.tokenize(tokenized)
    return [w.lower for w in tokenized if not re.match( "[^a-zA-Z\d\s€]",w)]


rows = c.execute('SELECT id, text from uitspraken').fetchall()

print("tokenize\n")
if not os.path.isfile('result.json'):
    print("new tokinizing")
    fp = open('result.json', 'w')
    texts = [tokenize(text) for id0, text in rows]
    json.dump(texts,fp)
else:
    print("used saved json")
    fp = open('result.json', 'r')
    texts = json.load(fp)

print(texts[0])

print("Now count frequencies\n")
#count frequencies
freqdist = nltk.FreqDist()
for text in texts:
    #for word in text:
    freqdist.update(text)

print("finished counting")
print(freqdist.most_common(50))
print(freqdist.hapaxes()[:50])


#Testjes voor tokenizing
# s = "1.5		ACM heeft bij besluit van 21 oktober 2010 (het primaire besluit) aan appellante een boete opgelegd van € 2.020.000,-- wegens overtreding van artikel 6, eerste lid, van de Mw."
# s = "ACM heeft bij besluit van 21 oktober 2010 (het primaire besluit) aan appellante een boete opgelegd van € 2.020.000,-- wegens overtreding van artikel 6, eerste lid, van de Mw"
# stemmer.stem('23a')
# print(tokenize(s))
