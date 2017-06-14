# coding: utf-8

# In[1]:

from __future__ import absolute_import
from lxml import etree
import re
import os
import sqlite3
import zipfile

# In[11]:

conn = sqlite3.connect(u'rechtspraak.db')
c = conn.cursor()

# In[3]:

# Create table
c.execute(u''' DROP TABLE IF EXISTS heldout_uitspraken''')
c.execute(u''' CREATE TABLE heldout_uitspraken
            (id text PRIMARY KEY,
            xml text,
            text text
            )
        ''')


# In[4]:

def retrieve_from_web(ecli):
    link = u'http://data.rechtspraak.nl/uitspraken/content?id=' + ecli
    try:
        return etree.ElementTree().parse(link)
    except Exception, e:
        print u'online retrieval fails' + link
        print e
        return None

# unzip uitspraken:
# for dir in 20*; do $(cd $dir && unzip "*.zip"); done

def retrieve_from_filesystem(ecli, rootpath):
    #zf = zipfile.ZipFile(rootpath)
    year = ecli[11:15]
    fn = unicode(year) + u'/' + re.sub(u':', u'_', ecli) + u'.xml'
    #file = (zf.open(fn))
    path = os.path.join(rootpath, fn).encode()
    try:
        return etree.ElementTree().parse(path)
    except Exception, e:

        #print('Exception: ', path)
        #print e
        return retrieve_from_web(ecli)
        #return None


# In[5]:

rootpath = u'/media/ylja/DATA/scriptie/open-data'


# In[ ]:

def insert_into_uitspraken(id0, element, curs):
    uitspraken = list(element.iterchildren(u'{*}uitspraak'))
    if len(uitspraken) > 0:
        uitspraak = uitspraken[0]
        uitspraak_xml = etree.tostring(uitspraak)
        # print uitspraak_xml
        uitspraak_text = u' '.join([e.text for e in uitspraak.iterdescendants() if e.text is not None])
        #print u'Dit is de uitspraak aan elkaar \n {0}' .format(uitspraak_text)
        # remove consecutive spaces
        uitspraak_text = re.sub(u' +', u' ', uitspraak_text)
        # print u'Dit is de uiteindelijke uitspraak text \n {0}' .format(uitspraak_text)
        query = ''' INSERT OR REPLACE INTO heldout_uitspraken
        VALUES (?, ?, ?)
        '''
        curs.execute(query, (id0, uitspraak_xml, uitspraak_text))


# In[ ]:

ids = c.execute(u'SELECT id from heldout_uitspraken_meta')
c2 = conn.cursor()
for row in ids:
    ecli = row[0]
    # el = retrieve_from_filesystem(ecli, rootpath)
    el = retrieve_from_web(ecli)
    if el is not None:
        insert_into_uitspraken(ecli, el, c2)
    else:
        print "nothing retrieved from web: " + unicode(ecli)
conn.commit()


c.execute(u'SELECT count(*) from heldout_uitspraken').fetchall()

conn.commit()
conn.close()




