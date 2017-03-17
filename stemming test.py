from pattern.text.nl import parsetree
import nltk

stemmer = nltk.stem.snowball.DutchStemmer(ignore_stopwords=True)

def stem(text):
    t = parsetree(text,tokenize=False,lemmata=True)
    return [lemma for lemma in [sent.lemmata for sent in t]]

def tokenize(text):
    tokenized = nltk.word_tokenize(text)
    return [stemmer.stem(w) for w in tokenized]

text = 'beschikking, beschikken, belanghebbende, belanghebben, zitting, zitten'
print stem(text)
print tokenize(text)