from __future__ import absolute_import

import re
import json
import os
import sqlite3
import logging
import codecs
from itertools import chain
import pattern.nl
import six

import gensim
import nltk
import nltk.tokenize
from io import open

from pattern.text.nl import parsetree

logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

conn = sqlite3.connect(u'rechtspraak.db')
c = conn.cursor()


#stemmer = nltk.stem.snowball.DutchStemmer(ignore_stopwords=True)
def tokenize(text):
    tokenized = nltk.word_tokenize(text)
    return [w for w in tokenized if not re.match( u'[^a-zA-uZ\d\s]',w)]

def stem(text):
    t = parsetree(text,tokenize=False,lemmata=True)
    return [lemma for lemma in [sent.lemmata for sent in t]]
    #return t



print 'fetch uitspraken'
rows =  c.execute(u'SELECT id, text from uitspraken LIMIT 10')
for row in rows:
    print row

# print u"tokenize"
# if not os.path.isfile(u'result.json'):
#     print u"new tokinizing"
#     fp = codecs.open('result.json', 'w', encoding='utf-8')
#     #texts = [unicode(tokenize(text)) for id0, text in rows]
#     texts = [text for id0, text in rows]
#     t = tokenize(texts[0])
#     #print 'stemming'
#     #t = (stem(texts[0]))
#     print t
#     #texts = [stem(text) for text in texts]
#     print 'dumping'
#     json.dump(t,fp, encoding='utf-8', ensure_ascii=False)
# else:
#     print u"used saved json"
#     fp = open(u'result.json', u'r')
#     texts = json.load(fp, encoding='utf-8')
#
# print texts[0]
#
# print u"Now count frequencies\n"


#count frequencies
# freqdist = nltk.FreqDist()
# for text in texts:
#     #for word in text:
#     freqdist.update(text)
#
# print("finished counting, remove 100 most common words and words occuring only once")
# common = freqdist.most_common(100)
# hapaxes = freqdist.hapaxes()



#
dictionary = gensim.corpora.Dictionary(texts)
print dictionary
#
# #removing words occuring in less than 5 documents, words appearing in more than 80% of the documents and the 100 most frequent words
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


#Testjes voor tokenizing
#words = stem(tokenize("De considerans, alsmede de artikelen 2, 4,5 en 13 van de Richtlijn 85/511/EEG van 18 november 1985 van de Europese Gemeenschappen, zoals gewijzigd in Richtlijn 90/423 van 26 juni 1990 tot vaststelling van gemeenschappelijke maatregelen ter bestrijding van mond- en klauwzeer, luiden, voor zover hier van belang, als volgt:"))

# stemmer.stem('23a')
# print(tokenize(s))
