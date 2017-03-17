import gensim
import json
import os
import codecs

readdir = '/media/ylja/DATA/scriptie/code/stemmeddocs/'
texts = []
for directory, subdirectories, files in os.walk(readdir):
    for f in files:
        path = readdir + f
        fp = codecs.open(path, 'r', encoding='utf-8')
        texts = texts.append(json.load(fp))

dictionary = gensim.corpora.Dictionary(texts)

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