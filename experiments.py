import gensim
import json
import os
import codecs
import logging



logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

moreThan = [0.5, 0.7, 0.9, 0,99]

def runLDA(less, more, mostfrequent):
    dictPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.dict'
    corpPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.mm'
    modPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.mm'
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    corpus = gensim.corpora.mmcorpus.MmCorpus(corpPath)
    tfidf = gensim.models.TfidfModel(corpus, id2word=dictionary)
    corpus_tfidf = tfidf[corpus] #trained model save
    print u"run LDA"
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, passes=3, id2word=dictionary)
    ldamodeltfidf = gensim.models.ldamodel.LdaModel(corpus, num_topics=100, passes=3, id2word=dictionary)
    #corpus_lda = ldamodel[corpus] #trained model save

    ldamodel.print_topics(num_topics=20)
    ldamodeltfidf.print_topics(num_topics=20)


for more in moreThan:
    runLDA(2, more, 100)
