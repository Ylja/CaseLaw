import gensim
from random import randint

topicpath = ''
dict = gensim.corpora.Dictionary.load('/media/ylja/DATA/scriptie/code/saveLDA/caseLaw20.99100.dict')
model = gensim.models.LdaModel.load('saveLDA/caseLaw50pass.model')

randomWord = dict.items()[randint(0,len(dict.items())-1)][1]


top_words = [[word for word, _ in model.show_topic(topicno, topn=10)] for topicno in range(model.num_topics)]

i = 0
for topic in top_words:
    print ("%s" % (' '.join(topic)))
    i += 1