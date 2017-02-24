
# coding: utf-8


import re
import os
import sqlite3
from lxml import etree




def get_entries_from_link(fr=0, maximum=1000, baselink=None):
    if baselink is None:
        baselink = 'http://data.rechtspraak.nl/uitspraken/zoeken?return=DOC&creator=http://standaarden.overheid.nl/owms/terms/Hoge_Raad_der_Nederlanden'
    #link = baselink+'&max='+str(maximum)+'&from='+str(fr)
    link = baselink+'&max='+str(maximum)+'&from='+str(fr)+ '&date=1913-01-01'+'&date=2016-12-31'

    xml_element = etree.ElementTree().parse(link)
    entries = list(xml_element.iter('{*}entry'))
    return entries


# ## Make a database



conn = sqlite3.connect('rechtspraak.db')



c = conn.cursor()



c.execute(''' DROP TABLE IF EXISTS uitspraken_meta''')
c.execute(''' CREATE TABLE uitspraken_meta
            (id text PRIMARY KEY,
            title text,
            summary text,
            updated text
            )
        ''')


# Now populate the table



def get_first_content(el, tag):
    return list(el.iter('{*}'+tag))[0].text

def insert_into_uitspraken_meta(entry, curs, table='uitspraken_meta'):
    id0 = get_first_content(entry, 'id')
    title = get_first_content(entry, 'title')
    summary = get_first_content(entry, 'summary')
    updated = get_first_content(entry, 'updated')
    query = ''' INSERT OR REPLACE INTO uitspraken_meta
        VALUES (?, ?, ?, ?)
    '''
    curs.execute(query, (id0, title, summary, updated))




size = 1000
end = 30000
for start in range(0, end, size):
    entries = get_entries_from_link(start, size)
    print(start, len(entries))
    for entry in entries:
        insert_into_uitspraken_meta(entry, c)




conn.commit()