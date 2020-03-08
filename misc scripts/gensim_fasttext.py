from pprint import pprint as print
from gensim.models.fasttext import FastText as FT_gensim
from gensim.test.utils import datapath
import time

# Set file names for train and test data
corpus_file = datapath('lee_background.cor')

model = FT_gensim(size=100)

start = time.time()

# build the vocabulary
model.build_vocab(corpus_file=corpus_file)

# train the model
model.train(
    corpus_file=corpus_file, epochs=model.epochs,
    total_examples=model.corpus_count, total_words=model.corpus_total_words
)

print(model)

print("Model trained")

print(str(model.most_similar("rest",topn=5)) + "\nTook " + str(time.time()-start))