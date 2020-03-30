#!/usr/bin/env python3

from gensim.parsing.preprocessing import (preprocess_string,remove_stopwords,
strip_multiple_whitespaces,strip_tags,strip_punctuation,strip_non_alphanum)
from gensim.models.word2vec import Word2Vec as w2v
import time
import os
from gensim import utils

# based on https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        # filter based on https://stackoverflow.com/questions/50009030/correct-way-of-using-phrases-and-preprocess-string-gensim
        custom_filter = [lambda x: x.lower(),remove_stopwords,strip_tags,strip_punctuation,strip_non_alphanum,strip_multiple_whitespaces,]
        corpus_path = "/home/zack/Desktop/Hons-Project/corpora/Westbury.Wikipedia.Corpus/WestburyLab.Wikipedia.Corpus.txt"
        # corpus_path = datapath("lee_background.cor")
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)
            # yield preprocess_string(line,filters=custom_filter)

if __name__ == "__main__":
    print("Training Model...")
    start = time.time()
    # train first skipgram model with hierarchical softmax
    model = w2v(sentences=MyCorpus(),workers=12,hs=1,sg=1)

    model_path = "/home/zack/Desktop/Hons-Project/models/w2v/w2v_wikipedia-skipgram.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    print("Model trained. Took " + str(round((time.time()-start),4)) + " seconds. Saving...")

    print(model.wv.most_similar("password",topn=5))

    # https://stackoverflow.com/questions/42399565/save-gensim-word2vec-model-in-binary-format-bin-with-save-word2vec-format
    # model.wv.save_word2vec_format(model_path, binary=True)
    model.save(model_path)

    # train second model with hiearchical softmax
    model = w2v(sentences=MyCorpus(),workers=12,hs=1,sg=0)

    model_path = "/home/zack/Desktop/Hons-Project/models/w2v/w2v_wikipedia-cbow.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    print("Model trained. Took " + str(round((time.time()-start),4)) + " seconds. Saving...")

    print(model.wv.most_similar("password",topn=5))

    # https://stackoverflow.com/questions/42399565/save-gensim-word2vec-model-in-binary-format-bin-with-save-word2vec-format
    # model.wv.save_word2vec_format(model_path, binary=True)
    model.save(model_path)

    # train third model with negative sampling
    model = w2v(sentences=MyCorpus(),workers=12,hs=0,sg=0)

    model_path = "/home/zack/Desktop/Hons-Project/models/w2v/w2v_wikipedia-cbow-hs0.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    print("Model trained. Took " + str(round((time.time()-start),4)) + " seconds. Saving...")

    print(model.wv.most_similar("password",topn=5))

    # https://stackoverflow.com/questions/42399565/save-gensim-word2vec-model-in-binary-format-bin-with-save-word2vec-format
    # model.wv.save_word2vec_format(model_path, binary=True)
    model.save(model_path)

    # train third model with negative sampling
    model = w2v(sentences=MyCorpus(),workers=12,hs=0,sg=1)

    model_path = "/home/zack/Desktop/Hons-Project/models/w2v/w2v_wikipedia-skipgram-hs0.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    print("Model trained. Took " + str(round((time.time()-start),4)) + " seconds. Saving...")

    print(model.wv.most_similar("password",topn=5))

    # https://stackoverflow.com/questions/42399565/save-gensim-word2vec-model-in-binary-format-bin-with-save-word2vec-format
    # model.wv.save_word2vec_format(model_path, binary=True)
    model.save(model_path)