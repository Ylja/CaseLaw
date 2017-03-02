from lxml import etree
import re
import json
import os
import sqlite3
import logging
#import lda
#from sklearn.feature_extraction.text import CountVectorizer
import itertools
import pandas as pd
import gensim
import nltk
import nltk.tokenize
from nltk.tokenize import MWETokenizer

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

conn = sqlite3.connect('rechtspraak.db')
c = conn.cursor()


#stemmer = nltk.stem.snowball.DutchStemmer(ignore_stopwords=True)
def tokenize(text):
    tokenized = nltk.word_tokenize(text)
    #return [stemmer.stem(w) for w in tokenized if w.isalnum()]
    #tokenizeMulti = MWETokenizer([('artikel', '6')])       #Kan dit met regex?
    #print(tokenized)
    #tokenized2 = tokenizeMulti.tokenize(tokenized)
    return [w.lower() for w in tokenized if not re.match( "[^a-zA-Z\d\s€]",w)]


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
# freqdist = nltk.FreqDist()
# for text in texts:
#     #for word in text:
#     freqdist.update(text)
#
# print("finished counting, remove 100 most common words and words occuring only once")
# common = freqdist.most_common(100)
# hapaxes = freqdist.hapaxes()




dictionary = gensim.corpora.Dictionary(texts)
print(dictionary)

#removing words occuring in less than 5 documents, words appearing in more than 80% of the documents and the 100 most frequent words
dictionary.filter_extremes(5, 0.5)
dictionary.
dictionary.filter_n_most_frequent(100)

#create bag of words for each doc.
print("prep done, creating bow")
corpus =  [dictionary.doc2bow(text) for text in texts]


#Do I need this?:
#  gensim.corpora.MmCorpus.serialize('/tmp/hr.mm', corpus)
print("bow done")

# tfidf = gensim.models.TfidfModel(corpus, id2word=dictionary)
# corpus_tfidf = tfidf[corpus]
print("run LDA")
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, passes=3, id2word=dictionary)
corpus_lda = ldamodel[corpus]

ldamodel.print_topics(num_topics = -1)


#Testjes voor tokenizing
# s = "1.5		ACM heeft bij besluit van 21 oktober 2010 (het primaire besluit) aan appellante een boete opgelegd van € 2.020.000,-- wegens overtreding van artikel 6, eerste lid, van de Mw."
# s = "ACM heeft bij besluit van 21 oktober 2010 (het primaire besluit) aan appellante een boete opgelegd van € 2.020.000,-- wegens overtreding van artikel 6, eerste lid, van de Mw"
# stemmer.stem('23a')
# print(tokenize(s))
