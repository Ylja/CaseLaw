from __future__ import absolute_import
import re
import sqlite3
import nltk
import codecs
import json



conn = sqlite3.connect(u'rechtspraak.db')
c = conn.cursor()



def tokenizing(text):
    tokenized = nltk.word_tokenize(text)
    return [w for w in tokenized if not re.match( u'[^a-zA-uZ\d\s]',w)]

rows =  c.execute(u'SELECT id, text from uitspraken')
for row in rows:
    file = 'docs/' + row[0] + '.json'
    fp = codecs.open(file, 'w', encoding='utf-8')
    t = tokenizing(row[1])
    json.dump(t, fp, encoding='utf-8', ensure_ascii=False)

#count frequencies
# freqdist = nltk.FreqDist()
# for text in texts:
#     #for word in text:
#     freqdist.update(text)
#
# print("finished counting, remove 100 most common words and words occuring only once")
# common = freqdist.most_common(100)
# hapaxes = freqdist.hapaxes()