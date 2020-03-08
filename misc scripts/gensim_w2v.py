from gensim.test.utils import datapath
from gensim import utils
import gensim.models
import time

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __iter__(self):
        corpus_path = datapath('lee_background.cor')
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)

start = time.time()

sentences = MyCorpus()
model = gensim.models.Word2Vec(sentences=sentences)

print("Model trained")

print(str(model.most_similar("rest",topn=5)) + "\nTook " + str(time.time()-start) + "s")