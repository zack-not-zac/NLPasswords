import re
import os
from autocorrect import Speller

if __name__ == "__main__":
    files = ["/home/zack/Desktop/Hons Project/program/corpora/twitter_cikm_2010/test_set_tweets.txt",
    "/home/zack/Desktop/Hons Project/program/corpora/twitter_cikm_2010/training_set_tweets.txt"]
    outpath = "/home/zack/Desktop/Hons Project/program/corpora/twitter_cikm_2010/filtered_tweet_text.txt"
    if os.path.isfile(outpath):
        print("File " + outpath + " already exists... removing.")
        os.remove(outpath)                                         # removes the file if it already exists.
        outfile = open(outpath,"a+")
    else:
        outfile = open(outpath,"a+")

    check = Speller(lang='en')

    for file in files:
        print("Opening: " + file)
        with open(file,"r") as f:
            for line in f:  
                line = line.split()
                for i,word in enumerate(line):
                    if re.search(r'[@][\w]',word) or re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',word):                  
                        line[i] = ''                                # removes twitter usernames and url's (URL expression from http://urlregex.com/)
                    elif re.match(r'[\d]{4}-[\d]{2}-[\d]{2}',word): # if string contains date in form 2000-01-01
                        tweet_text = line[3:i]                      # sets tweet_text to everything between the 3rd element (eliminating garbage) and the date (end of tweet)
                        corrected = []                              # empty list for spell check
                        for spellcheck_word in tweet_text:
                            if not re.match(r'[0-9]',spellcheck_word):         # if the word contains a number, we don't want to autocorrect it
                                corrected.append(check(spellcheck_word))       # appends each corrected word to the line
                            else:
                                corrected.append(spellcheck_word)
                        tweet = ' '.join(corrected)                 # joins the tweet back together as a string
                        tweet += "\n"                               # adds newline char to end of string
                        outfile.write(tweet)                        # writes to the output file

    outfile.close()
    exit()