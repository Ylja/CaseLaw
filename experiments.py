import gensim
import json
import codecs
import logging



logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

moreThan = [0.99]

def runLDA(less, more, mostfrequent):
    # dictPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.dict'
    dictPath = 'saveLDA/caseLaw20.99100.dict'
    corpPath = 'saveLDA/caseLaw20.99100.mm'
    #corpPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.mm'
    dictionary = gensim.corpora.Dictionary.load(dictPath)
    corpus = gensim.corpora.mmcorpus.MmCorpus(corpPath)
    #tfidf = gensim.models.TfidfModel(corpus, id2word=dictionary)
    #corpus_tfidf = tfidf[corpus] #trained model save
    print u"run LDA"
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=50, passes=50, id2word=dictionary)

    #corpus_lda = ldamodel[corpus] #trained model save
    print '\n\nLDA'
    topics = ldamodel.print_topics(num_topics=-1)
    path = 'saveLDA/topics50passes10prep' + str(more) + '.json'
    fp = codecs.open(path, 'w', encoding='utf-8')
    json.dump(topics, fp)
    ldamodel.save('saveLDA/caseLaw50pass.model')



for more in moreThan:
    runLDA(2, more, 100)
