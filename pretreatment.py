from gensim import corpora, models, similarities
from pprint import pprint
from collections import defaultdict
from gensim.similarities import Similarity
import treetaggerwrapper, json, string, gensim, time, pickle, marshal

t1 = time.time()

#DETERMINANTS
def Read(path):
    import csv
    import codecs
    with codecs.open(path, 'rU', encoding='utf-8', errors = 'ignore') as csvfile:
        return list(csv.DictReader(csvfile, delimiter = ";"))

reader = Read('det.csv')
base = []
for row in reader:
    det = row['determinant']
    base.append(det)

#Fonctions
def remove_punctuation(from_text):
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in from_text]
    return stripped

def doublons(list):
    double = True
    while double == True: 
        double = False 
        liste_verif = [] 
        for word in list:
            try: 
                doublon = liste_verif.index(word) 
                list.remove(word)  
                double = True 
            except: pass 
            liste_verif.append(word)
    return list

class TreeTaggerWord:
    def __init__(self, triplet):
        self.word,self.postag,self.lemma = triplet

def format(output):
    words = []
    for w in output:
        words.append(TreeTaggerWord(w.split("\t")))
    return words
    
#Messages
with open('testbow.json', encoding='utf8') as f:
    data = json.load(f)

dicti = {}
for things in data['Messages']:
    num = things['MessageNumber']
    msg = things['LongText']
    u = 0
    while u < len(things):
        dicti[num] = msg
        u += 1

#Tri & fréquence
numbers = dicti.keys()
message = dicti.values()

num_list = []
for num in numbers:
    num_list.append(num)

marshal.dump(num_list, open("list_numbers", 'wb'))
 
docs = [[word for word in document.lower().replace("'", ' ').replace(".", ' ').replace(",", ' ').split() if word not in base]
        for document in message] 
doc = [remove_punctuation(i) for i in docs]

lemmat = []
p = 0
while p < len(doc):    
    for word in doc[p]:
        if word == '':
            doc[p].remove(word)
    tt_fr = treetaggerwrapper.TreeTagger(TAGLANG = 'fr')
    tag = tt_fr.tag_text(doc[p])
    pprint(tag)
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
            if doc[p][i].isdigit() == False and doc[p][i] != lemmat[i]:
                doc[p][i] = lemmat[i]
            i += 1
    except:
        doc[p] = doc[p]
    lemmat = []
    p += 1

with open('liste_msg', 'wb') as file:
    liste_msg = pickle.Pickler(file)
    liste_msg.dump(doc)

counting = len(dicti)
frequency = defaultdict(int)
for texte in doc:
    doublons(texte)
    for token in texte:
        frequency[token] += (1 * 100)/counting
        frequency[token] = round(frequency[token], 3)
        if frequency[token] > 30:
            if token not in base:
                base.append(token)

marshal.dump(base, open("list_base", 'wb'))

#Dictionnaire spécifique
texts = [[token for token in texte if frequency[token] < 50]
        for texte in doc]

dictionary = corpora.Dictionary(texts)
dictionary.save('specifiques.dict')

#Vectorisation
with open('liste_msg', 'rb') as file:
     extraction = pickle.Unpickler(file)
     extract = extraction.load()

corpus = [dictionary.doc2bow(text) for text in extract]
corpora.MmCorpus.serialize('specifiques.mm', corpus)

class MyCorpus(object):
    def __iter__(self):
        for line in message:
            yield dictionary.doc2bow(line.lower().split())
        
corpus_memory_friendly = MyCorpus()

print(time.time() - t1)

#TF-IDF & Similarités
tfidf = models.TfidfModel(corpus)

index = similarities.MatrixSimilarity(tfidf[corpus])
index.save('similarities.index')

print(time.time() - t1)
