import gensim
import numpy


corpus = gensim.corpora.mmcorpus.MmCorpus('saveLDA/caseLaw20.99100.mm')

uniquelen = 0
len = 0
corpuslen = corpus.__len__()
wordcount = []
uniquewordcount = []


for l in corpus:
    numberofuniquewords = l.__len__()
    numberofwords = 0
    for word, freq in l:
        numberofwords+=freq
    len += numberofwords
    uniquelen += numberofuniquewords
    wordcount.append(numberofwords)
    uniquewordcount.append(numberofuniquewords)


print "average number of words: " + str(len/corpuslen)
print "average number of unique words: " + str(uniquelen/corpuslen)
print "median number of words: " + str(numpy.median(wordcount.sort()))
print "median number of unique words: " + str(numpy.median(uniquewordcount.sort()))

