from nltk.corpus import wordnet

synonyms = wordnet.synsets("graveyard")

if len(synonyms) < 1:
    print("No results found")

for i in synonyms:
    print(i.lemmas()[0].name())