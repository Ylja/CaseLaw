
# coding: utf-8


from __future__ import absolute_import
import re
import os
import sqlite3
from lxml import etree




def get_entries_from_link(fr=0, maximum=1000, baselink=None):
    if baselink is None:
        baselink = u'http://data.rechtspraak.nl/uitspraken/zoeken?return=DOC&creator=http://standaarden.overheid.nl/owms/terms/Hoge_Raad_der_Nederlanden'
    #link = baselink+'&max='+str(maximum)+'&from='+str(fr)
    link = baselink+u'&max='+unicode(maximum)+u'&from='+unicode(fr)+ u'&date=1913-01-01'+u'&date=2016-12-31'
    xml_element = etree.ElementTree().parse(link)
    entries = list(xml_element.iter(u'{*}entry'))
    return entries


# ## Make a database



conn = sqlite3.connect(u'rechtspraak.db')



c = conn.cursor()


print 'begin\n'
c.execute(u''' DROP TABLE IF EXISTS uitspraken_meta''')
c.execute(u''' CREATE TABLE uitspraken_meta
            (id text PRIMARY KEY,
            title text,
            summary text,
            updated text
            )
        ''')


# Now populate the table



def get_first_content(el, tag):
    return list(el.iter(u'{*}'+tag))[0].text

def insert_into_uitspraken_meta(entry, curs, table=u'uitspraken_meta'):
    id0 = get_first_content(entry, u'id')
    title = get_first_content(entry, u'title')
    summary = get_first_content(entry, u'summary')
    updated = get_first_content(entry, u'updated')
    query = u''' INSERT OR REPLACE INTO uitspraken_meta
        VALUES (?, ?, ?, ?)
    '''
    curs.execute(query, (id0, title, summary, updated))




size = 1000
end = 30000
for start in xrange(0, end, size):
    entries = get_entries_from_link(start, size)
    print '{0} {1}\n' .format(start, len(entries))
    for entry in entries:
        insert_into_uitspraken_meta(entry, c)




conn.commit()