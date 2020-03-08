from os import path,removedirs,remove,mkdir
from gensim.models import Word2Vec, FastText
from time import time

directory = "/home/zack/Desktop/Hons Project/program/models/results/"
topn = 10
start = time()
words = []

w2v = Word2Vec.load("/home/zack/Desktop/Hons Project/program/models/w2v/w2v_twitteronly.model")
ft = FastText.load("/home/zack/Desktop/Hons Project/program/models/fasttext/ft_twitteronly.model")

print("models loaded successfully!")

if path.exists(directory + "w2v_results.txt"):
    remove(directory + "w2v_results.txt")

w2v_outfile = open(directory + "w2v_results.txt","a+")

if path.exists(directory + "ft_results.txt"):
    remove(directory + "ft_results.txt")

ft_outfile = open(directory + "ft_results.txt","a+")

with open("/home/zack/Desktop/Hons Project/program/models/testwords.txt","r") as f:
    for line in f:
        words.append(line.strip())
        
print(len(words))

# words = ['time','person','year','way','day','thing','man','world','life','hand']
# words += ['password','dragon','baseball','superman','secret','computer','shadow','master']

for word in words:
    w2v_result = str(w2v.wv.most_similar(word,topn=topn))
    ft_result = str(ft.wv.most_similar(word,topn=topn))
    w2v_outfile.write("Word: " + word + "\nMost similar: \n" + w2v_result + "\n\n")
    ft_outfile.write("Word: " + word + "\nMost similar: " + ft_result + "\n\n")

w2v_outfile.close()
ft_outfile.close()

print("Test complete. Took " + str(round(time()-start,3)) + " seconds.")