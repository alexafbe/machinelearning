from gensim import corpora, models, similarities
from pprint import pprint
from collections import defaultdict
from gensim.similarities import Similarity
import json, string, gensim, time, pickle, marshal

t1 = time.time()

#TF-IDF & Similarités
index = similarities.MatrixSimilarity.load('similarities.index')
numbers = marshal.load(open("list_numbers", "rb"))
vec_new_msg = marshal.load(open("vec_nv", "rb"))

sims = index[vec_new_msg]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

q = 0
while q < 3:
    val = sims[q][0]
    print(sims[q])
    print(numbers[val])
    q += 1

print(time.time() - t1)