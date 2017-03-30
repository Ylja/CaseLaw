
# coding: utf-8

# In[1]:

from __future__ import division
from __future__ import absolute_import
import re
import os
import sqlite3
import pandas as pd


# In[2]:

conn = sqlite3.connect(u'rechtspraak.db')
c = conn.cursor()


# In[3]:

#pd.DataFrame(c.execute('''SELECT * FROM uitspraken_meta''').fetchmany(10))


# In[5]:

#print(pd.DataFrame(c.execute('''SELECT min(updated), max(updated) FROM uitspraken_meta''').fetchall()))


# number of uitspraken_meta

s = c.execute(u'SELECT COUNT(*) FROM UITSPRAKEN_META').fetchall()[0]
print u'\'Uitspraken\' with Metadata: '+ unicode(s[0])

#How many 'uitspraken' do we have?
print u'\'Uitspraken\': '+unicode(c.execute(u'''select count(*) from uitspraken''').fetchall()[0])


# sort by summary

# summary_counts = c.execute(''' SELECT * FROM (
#                 SELECT SUMMARY, COUNT(*) AS cnt
#                 FROM UITSPRAKEN_META
#                 GROUP BY SUMMARY
#             ) ORDER BY CNT DESC
# ''') #.fetchall()
# pd.DataFrame(summary_counts.fetchmany(20))


# In[7]:
#
# lenid_counts = c.execute(''' SELECT length(id), count(*) FROM UITSPRAKEN_META group by length(id)
# ''')
# pd.DataFrame(lenid_counts.fetchall())


# In[8]:

def nr_of_fields_id(text):
    return len(text.split(u':'))

def year_from_id(text):
    return text.split(u':')[3]

def instantie_from_id(text):
    return text.split(u':')[2]

conn.create_function(u'nr_of_fields_id', 1, nr_of_fields_id)
conn.create_function(u'year_from_id', 1, year_from_id)
conn.create_function(u'instantie_from_id', 1, instantie_from_id)
conn.commit()


# In[9]:

# ECLIs = c.execute('SELECT id FROM uitspraken_meta where year_from_id(id) = 2014').fetchmany(10)
# ECLIs = [s[0] for s in ECLIs]
# ECLIs




# nrfields_counts = c.execute(''' SELECT nr_of_fields_id(id), count(*) FROM UITSPRAKEN_META group by nr_of_fields_id(id)
# ''')
# pd.DataFrame(nrfields_counts.fetchall())


wc = c.execute(u'''SELECT length(text) - length(replace(text, ' ', '')) + 1 FROM UITSPRAKEN''')
sum = 0
amount = 0
for text in wc.fetchall():
    sum+= text[0]
    amount += 1
avg = sum/amount
print u'Average amount of words in \'uitspraken\': ' + unicode(avg) + u'\n'


#  from which courts do the 'uitspraken come from?'

instantie_counts = c.execute(u''' SELECT instantie_from_id(id), count(*) 
                FROM UITSPRAKEN_META group by instantie_from_id(id) 
''')
print pd.DataFrame(instantie_counts.fetchall())


# From which year are the 'uitspraken'

year_counts = c.execute(u''' SELECT year_from_id(id), count(*) 
                FROM UITSPRAKEN_META group by year_from_id(id) 
                order by year_from_id(id) 
''')
print pd.DataFrame(year_counts.fetchall())


# In[15]:






# In[37]:

c.close()


# In[ ]: