# coding: utf-8

# In[1]:

from lxml import etree
import re
import os
import sqlite3
import zipfile

# In[11]:

conn = sqlite3.connect('rechtspraak.db')
c = conn.cursor()

# In[3]:

# Create table
c.execute(''' DROP TABLE IF EXISTS uitspraken''')
c.execute(''' CREATE TABLE uitspraken
            (id text PRIMARY KEY,
            xml text,
            text text
            )
        ''')


# In[4]:

def retrieve_from_web(ecli):
    link = 'http://data.rechtspraak.nl/uitspraken/content?id=' + ecli
    try:
        return etree.ElementTree().parse(link)
    except Exception as e:
        print('online retrieval fails' + link)
        print(e)
        return None

# unzip uitspraken:
# for dir in 20*; do $(cd $dir && unzip "*.zip"); done

def retrieve_from_filesystem(ecli, rootpath):
    #zf = zipfile.ZipFile(rootpath)
    year = ecli[11:15]
    fn = str(year) + '/' + re.sub(':', '_', ecli) + '.xml'
    #file = (zf.open(fn))
    path = os.path.join(rootpath, fn)
    try:
        return etree.ElementTree().parse(path)
    except Exception as e:

        #print('Exception: ', path)
        print(e)
        return retrieve_from_web(ecli)
        #return None


# In[5]:

rootpath = '/home/ylja/Uni/Thesis/OpenData'


# In[ ]:

def insert_into_uitspraken(id0, element, curs):
    uitspraken = list(element.iterchildren('{*}uitspraak'))
    if len(uitspraken) > 0:
        uitspraak = uitspraken[0]
        uitspraak_xml = etree.tostring(uitspraak)
        uitspraak_text = ' '.join([e.text for e in uitspraak.iterdescendants() if e.text is not None])
        # remove consecutive spaces
        uitspraak_text = re.sub(' +', ' ', uitspraak_text)
        query = ''' INSERT OR REPLACE INTO uitspraken
        VALUES (?, ?, ?)
        '''
        curs.execute(query, (id0, uitspraak_xml, uitspraak_text))


# In[ ]:

ids = c.execute('SELECT id from uitspraken_meta')
c2 = conn.cursor()
for row in ids:
    ecli = row[0]
    el = retrieve_from_filesystem(ecli, rootpath)
    if el is not None:
        insert_into_uitspraken(ecli, el, c2)
conn.commit()

# In[12]:

c.execute('SELECT count(*) from uitspraken').fetchall()

# In[13]:

conn.commit()
conn.close()


# In[ ]:


