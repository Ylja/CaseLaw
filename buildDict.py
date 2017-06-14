import gensim
import json
import os
import codecs
import logging
from cStringIO import StringIO

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


logging.basicConfig(format=u'%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


file = open('/media/ylja/DATA/scriptie/code/stopwords.txt', 'r')
t = file.read()
stopwords = t.splitlines()
stopwords[0]= 'aan'



def concats(text):
    file_str = StringIO()
    for word in text:
        file_str.write(word)
    return file_str.getvalue()

def removeStopWord(text):
    # return [word for word in text if not stopwords.__contains__(word)]
    return text


if not os.path.isfile('/media/ylja/DATA/scriptie/code/texts.json'):
    skip = 0
    read = 0
    print "oh no"
    readdir = '/media/ylja/DATA/scriptie/code/docs/'
    texts = []
    for directory, subdirectories, files in os.walk(readdir):
        for f in files:
            path = readdir + f
            if os.stat(path).st_size > 5000:
                fp = codecs.open(path, 'r', encoding='utf-8')
                text = json.load(fp)
                # t = [concats(word) for word in text]
                texts.append(removeStopWord(text))
                fp.close()
                read += 1
            else:
                print 'skipped: ' + path
                skip += 1

    write = codecs.open('/media/ylja/DATA/scriptie/code/texts.json', 'w', encoding='utf-8')
    json.dump(texts, write)
    print '\nWe have skipped ' + str(skip) + ' files that were empty or smaller than 5000 bytes'
    print 'We have read ' + str(read) + ' docs\n'
    print texts[0]
else:
    print "yay"
    fp =  codecs.open('/media/ylja/DATA/scriptie/code/texts.json', 'r', encoding='utf-8')
    t = json.load(fp)
    texts = [removeStopWord(text) for text in t]

dictionary = gensim.corpora.Dictionary(texts)
dictionary.save('saveLDA/caseLawBase.dict')

# #removing words occuring in less than 2 documents, words appearing in more than 99% of the documents and the 100 most frequent words and a stop word list
def createDictAndCorpus(less, more, mostfrequent,texts):
    #build dict
    dict = gensim.corpora.Dictionary(texts)
    frequentwords = dict.filter_n_most_frequent(mostfrequent)
    print(frequentwords)
    extremes = dict.filter_extremes(less, more, None)
    # dictPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.dict'
    # dict.save(dictPath)
    # #build corpus
    # corpus = [dict.doc2bow(text) for text in texts]
    # corpPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.mm'
    # gensim.corpora.MmCorpus.serialize(corpPath, corpus)
    # #save removed words
    # remWordsPath = 'saveLDA/caseLaw' + str(less) + str(more) + str(mostfrequent) + '.json'
    # fp = codecs.open(remWordsPath, 'w', encoding='utf-8')
    # json.dump((frequentwords, extremes), fp)
    # fp.close()



#different word removal

moreThan = [0.99]


for more in moreThan:
    createDictAndCorpus(2, more, 100, texts)



