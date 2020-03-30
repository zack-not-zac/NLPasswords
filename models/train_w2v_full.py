#!/usr/bin/env python3

from gensim.parsing.preprocessing import (preprocess_string,remove_stopwords,
strip_multiple_whitespaces,strip_tags,strip_punctuation,strip_non_alphanum)
from gensim.models.word2vec import Word2Vec as w2v
import time
import os
from gensim import utils

#TODO: train as skipgram using hierarchical softmax and increased dimensionality

# based on https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        # filter based on https://stackoverflow.com/questions/50009030/correct-way-of-using-phrases-and-preprocess-string-gensim
        # custom_filter = [lambda x: x.lower(),remove_stopwords,strip_tags,strip_punctuation,strip_non_alphanum,strip_multiple_whitespaces,]
        corpus_path = "/home/zack/Desktop/Hons-Project/corpora/combined_corpus.txt"
        # corpus_path = datapath("lee_background.cor")
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)
            # yield preprocess_string(line,filters=custom_filter)

if __name__ == "__main__":
    print("Training Model...")
    start = time.time()
    model = w2v(sentences=MyCorpus(),workers=12,min_count=10,sg=1,hs=1,size=150)

    model_path = "/home/zack/Desktop/Hons-Project/models/w2v/w2v_wikipedia_and_reddit_comments.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    print("Model trained. Took " + str(round((time.time()-start),2)) + " seconds. Saving...")

    # https://stackoverflow.com/questions/42399565/save-gensim-word2vec-model-in-binary-format-bin-with-save-word2vec-format
    # model.wv.save_word2vec_format(model_path, binary=True)#
    try:
        model.save(model_path)
    except FileNotFoundError:
        model.save("w2v_wikipedia_and_reddit_comments.model") # dump here
