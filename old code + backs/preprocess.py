from __future__ import absolute_import
from lxml import etree
import re
import json
import os
import sqlite3
import logging
import pattern.nl
import six



import gensim
import nltk
import nltk.tokenize
from io import open


logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

conn = sqlite3.connect(u'rechtspraak.db')
c = conn.cursor()


#stemmer = nltk.stem.snowball.DutchStemmer(ignore_stopwords=True)
def tokenize(text):
    tokenized = nltk.word_tokenize(text)
    #return [stemmer.stem(w) for w in tokenized if w.isalnum()]
    #tokenizeMulti = MWETokenizer([('artikel', '6')])       #Kan dit met regex?
    #print(tokenized)
    #tokenized2 = tokenizeMulti.tokenize(tokenized)
    return [unicode(w.lower()) for w in tokenized if not re.match( u'[^a-zA-uZ\d\s]',w)] # nEED to declare encoding


rows = c.execute(u'SELECT id, text from uitspraken').fetchall()

print u"tokenize\n"
if not os.path.isfile(u'result.json'):
    print u"new tokinizing"
    fp = open(u'result.json', u'w')
    #texts = [tokenize(text) for id0, text in rows]
    texts = tokenize(rows[0][1])
    print texts
    #json.dump(unicode(texts),fp)
else:
    print u"used saved json"
    fp = open(u'result.json', u'r')
    texts = json.load(fp)

print texts[0]

print u"Now count frequencies\n"
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
print dictionary

#removing words occuring in less than 5 documents, words appearing in more than 80% of the documents and the 100 most frequent words
dictionary.filter_extremes(5, 0.5)
dictionary.filter_n_most_frequent(100)

#create bag of words for each doc.
print u"prep done, creating bow"
corpus =  [dictionary.doc2bow(text) for text in texts]


#Do I need this?:
#  gensim.corpora.MmCorpus.serialize('/tmp/hr.mm', corpus)
print u"bow done"

# tfidf = gensim.models.TfidfModel(corpus, id2word=dictionary)
# corpus_tfidf = tfidf[corpus]
print u"run LDA"
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, passes=3, id2word=dictionary)
corpus_lda = ldamodel[corpus]

ldamodel.print_topics(num_topics = -1)



