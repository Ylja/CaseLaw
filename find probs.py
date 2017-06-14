import gensim
import json
import codecs
from cStringIO import StringIO
import logging
from random import randint
import os

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


dict = gensim.corpora.Dictionary.load('/media/ylja/DATA/scriptie/code/saveLDA/caseLaw20.99100.dict')
model = gensim.models.LdaModel.load('/media/ylja/DATA/scriptie/code/saveLDA/caseLaw20.99100.model')

fp = codecs.open('/media/ylja/DATA/scriptie/code/texts.json', 'r', encoding='utf-8')
texts = json.load(fp)

def concats(text):
    file_str = StringIO()
    for word in text:
        try:
            file_str.write(str(word))
        except UnicodeEncodeError:
            print '\n oops \n'
    return file_str.getvalue()

def flat(text):
    return [word[0] for word in text]

readdir = '/media/ylja/DATA/scriptie/code/stemmeddocs/'

eclis = [("ECLI:NL:HR:2014:2773.json", 43), ("ECLI:NL:HR:2011:BP3968.json",16), ("ECLI:NL:HR:2011:BP4800.json",35), ("ECLI:NL:HR:2008:BD1842.json",34), ("ECLI:NL:HR:2001:AB2151.json",45), ("ECLI:NL:HR:2002:AD9487.json",17), ("ECLI:NL:HR:2014:3303.json",2), ("ECLI:NL:HR:1998:AA2396.json",31), ("ECLI:NL:HR:2014:1303.json",5), ("ECLI:NL:HR:2013:BZ7150.json",42)]
# eclis = [("ECLI:NL:HR:2014:2773.json", 43)]
for ecli, intruder in eclis:
    path = readdir + ecli
    fp = codecs.open(path, 'r', encoding='utf-8')
    text = json.load(fp)
    t = flat(text)
    bow = dict.doc2bow(t)

    tops = sorted(model.get_document_topics(bow,minimum_probability=0.00000000000001), key=lambda x: x[1], reverse=True)
    topics = [(i,p) for i, p in tops if not i in [7,19,28,44]]
    print '\n\nECLI: ' + ecli
    ids = []
    for topicid, prob in topics[:3]:
        print '\nTopic ' + str(topicid) + ' with probability: ' + str(prob)
        words = [word for (word, _) in model.show_topic(topicid, topn=10)]
        for w in words:
            print w,
    topics = [(i, p) for i, p in tops if i is intruder]
    for i, p in topics:
        print str(i)  + " prob: " + str(p)
