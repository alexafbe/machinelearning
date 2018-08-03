from gensim import corpora, models, similarities
from pprint import pprint
from collections import defaultdict
from gensim.similarities import Similarity
import treetaggerwrapper, string, gensim, time, pickle, marshal

#FONCTIONS & FICHIERS
def remove_punctuation(from_text):
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in from_text]
    return stripped

class TreeTaggerWord:
    def __init__(self, triplet):
        self.word,self.postag,self.lemma = triplet

def format(output):
    words = []
    for w in output:
        words.append(TreeTaggerWord(w.split("\t")))
    return words

t1 = time.time()

dictionary = corpora.Dictionary.load('specifiques.dict')
corpus = corpora.MmCorpus('specifiques.mm')
index = similarities.MatrixSimilarity.load('similarities.index')
numbers = marshal.load(open("list_numbers", "rb"))
base = marshal.load(open("list_base", "rb"))

print(base)

tfidf = models.TfidfModel(corpus)

mes = input("Veuillez saisir votre message :")

mess = []
lemmat = []
if num in numbers:
    doc = remove_punctuation(msg.lower().replace("'", ' ').replace(".", ' ').replace(",", ' ').split())
    for word in doc:
        if word == '':
            doc.remove(word)
        tt_fr = treetaggerwrapper.TreeTagger(TAGLANG = 'fr')
        tag = tt_fr.tag_text(doc)
        data = format(tag)
        z = 0
        while z < len(tag):
            lemmat.append(data[z].lemma)
            z += 1
        for val in lemmat:
            if val == '°':
                lemmat.remove(val)
            elif val == '-':
                lemmat.remove(val)
        i = 0
        try:
            while i < len(lemmat):
                if doc[i].isdigit() == False and doc[i] != lemmat[i]:
                    doc[i] = lemmat[i]
                i += 1
        except:
            doc = doc
        lemmat = []
    i = 0
    while i < len(message):
        if message[i] not in base:
            mess.append(message[i])
        i += 1
    vec_bow = dictionary.doc2bow(mess)
    vec_new_msg = tfidf[vec_bow]

marshal.dump(vec_new_msg, open('vec_nv', 'wb'))

print(time.time() - t1)