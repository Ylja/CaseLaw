import os
from pattern.text.nl import parsetree
import json
import codecs

readdir =  '/media/ylja/DATA/scriptie/code/heldoutdocs/'
writedir = '/media/ylja/DATA/scriptie/code/heldoutdocs/stemmeddocs/'

def stem(text):
    t = parsetree(text,tokenize=False,lemmata=True)
    return [lemma for lemma in [sent.lemmata for sent in t]]


for directory, subdirectories, files in os.walk(readdir):
    for f in files:
        if not f == 'ECLI:NL:HR:2001:AB1453.json':
            rfile = readdir + f
            wfile = writedir + f
            if not os.path.isfile(wfile):
                rfp = codecs.open(rfile, 'r', encoding='utf-8')
                text = json.load(rfp)
                wfp = codecs.open(wfile, 'w', encoding='utf-8')
                stemmed = stem(text)
                json.dump(stemmed,wfp, encoding='utf-8', ensure_ascii=False)





