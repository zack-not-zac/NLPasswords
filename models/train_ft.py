#!/usr/bin/env python3

from gensim.parsing.preprocessing import preprocess_string,remove_stopwords,strip_multiple_whitespaces,strip_tags,strip_punctuation,strip_non_alphanum
from gensim.models.fasttext import FastText as ft
import time
import os
import re
from autocorrect import Speller


# based on https://radimrehurek.com/gensim/models/fasttext.html

speller = Speller(lang='en')

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __iter__(self):
        # filter based on https://stackoverflow.com/questions/50009030/correct-way-of-using-phrases-and-preprocess-string-gensim
        custom_filter = [lambda x: x.lower(),remove_stopwords,strip_tags,strip_punctuation,strip_non_alphanum,strip_multiple_whitespaces]
        corpus_path = "/home/zack/Desktop/Hons Project/program/corpora/twitter_cikm_2010/filtered_tweet_text.txt"
        # corpus_path = datapath("lee_background.cor")
        for line in open(corpus_path):
            correctedline = []
            for word in line.split(" "):
                if not re.match(r'[0-9]',word):         # if the word contains a number, we don't want to autocorrect it
                    correctedline.append(speller(word)) # appends each corrected word to the line
            line = " ".join(correctedline)              # stitch the line back together    
            # assume there's one document per line, tokens separated by whitespace
            # yield utils.simple_preprocess(line)
            yield preprocess_string(line,filters=custom_filter)

if __name__ == "__main__":
    print("Training Model...")
    start = time.time()
    model = ft(workers=12)
    model.build_vocab(sentences=MyCorpus())
    total_examples = model.corpus_count

    model_path = "/home/zack/Desktop/Hons Project/program/models/fasttext/ft_twitteronly.model"
    if os.path.exists(model_path):
        os.remove(model_path)
    
    model.train(sentences=MyCorpus(),total_examples=total_examples, epochs=5)

    print("Model trained. Took " + str(round((time.time()-start),4)) + " seconds. Saving...")

    model.save(model_path)