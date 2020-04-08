#!/usr/bin/env python3

from gensim.models import Word2Vec as w2v
from nltk.corpus import stopwords
from sys import argv
import re
from time import time

possible_passwords = set()          # a set is used as it does not allow for duplicate entries & allows for efficient searching
has_numbers = True                  # numbers flag for passwords
has_special_chars = True            # special chars for passwords
use_nlp = True                      # use NLP model
max_length = 0                      # max password length
min_length = 0                      # min password length (default is set to length of previous password)
model = None                        # variable for storing NLP model
max_passwords = 0                   # max passwords outputted by the program 
model_path = "models/w2v/w2v_wikipedia_and_reddit_comments.model"
ascii_art = """ __   __     __         ______   ______     ______     ______     __     __     ______     ______     _____     ______    
/\ \"-.\ \   /\ \       /\  == \ /\  __ \   /\  ___\   /\  ___\   /\ \  _ \ \   /\  __ \   /\  == \   /\  __-.  /\  ___\   
\ \ \-.  \  \ \ \____  \ \  _-/ \ \  __ \  \ \___  \  \ \___  \  \ \ \/ \".\ \  \ \ \/\ \  \ \  __<   \ \ \/\ \ \ \___  \  
 \ \_\\\" \_\  \ \_____\  \ \_\    \ \_\ \_\  \/\_____\  \/\_____\  \ \__/\".~\_\  \ \_____\  \ \_\ \_\  \ \____-  \/\_____\ 
  \/_/ \/_/   \/_____/   \/_/     \/_/\/_/   \/_____/   \/_____/   \/_/   \/_/   \/_____/   \/_/ /_/   \/____/   \/_____/ 
                                                                                                                          """

def replace_all_occurences_forward(pw,char,sub,pos):
    s = pw[pos:]                                # clips string from pos forward
    s_before = pw[:pos]                         # takes the chars from before pos
    s = s_before + s.replace(char,sub)          # stitches string back together with all substitutions after pos implemented
    return s

def append_to_set(s):
    for item in s:
        if len(item) <= max_length or max_length == 0 and len(item) >= min_length:  # if the string is less than max length or more than min length, max length = 0 (no limit)
            possible_passwords.add(item)                                            # add to possible_passwords

def append_string_to_set(s):
    if len(s) <= max_length or max_length == 0 and len(s) >= min_length:            # if the string is less than max length or more than min length, max length = 0 (no limit)
            possible_passwords.add(s)                                            # add to possible_passwords

def put_char_in_pos(sub,pos,pw):
    temp = list(pw)                             # convert pw into list
    temp[pos] = sub[1]                          # change char to substitute
    s = ''.join(temp)                           # join list back into str
    return s

def char_substitution(word, max_words_generated):
    substituted_passwords = set()
    chars = {       # dictionary for char substitutions (https://code.sololearn.com/ceEeO2m4wGBG/#py)
        "a":"4,@",
        "b":"6",
        "e":"3,€",
        "g":"6,9",
        "i":"1,!",
        "l":"1",
        "o":"0",
        "s":"5,$",
        "t":"7",
        "z":"2,5"}

    print("Performing character substitution on " + word + "...")

    substitutions = set()
    for char in word:                                                       # for each character in password
        if chars.get(char.lower()) != None:                                 # if a substitution exists
            for char_substitute in chars.get(char.lower()).split(','):      # get all substitutions
                if not has_numbers:                                         # if pw shouldn't have numbers
                    if not re.match(r'\d',char_substitute):                 # if sub doesnt have numbers
                        substitutions.add((char.lower(),char_substitute))   # add substitution to list
                elif not has_special_chars:                                 # if pw shouldn't have special chars
                    if not re.match(r'\W',char_substitute):                 # if sub doesnt have non-word chars
                        substitutions.add((char.lower(),char_substitute))
                else:
                    substitutions.add((char.lower(),char_substitute)) 
    for sub in substitutions:
        positions = [x for x,v in enumerate(word) if v.lower() == sub[0]]   # get all positions char (v) exists
        for pos in positions:                                               # for each position
            substituted_passwords.add(put_char_in_pos(sub,pos,word))        # swap chars and add to list
            if len(substituted_passwords) > max_words_generated and max_words_generated != 0:   
                return substituted_passwords                                # if i exceeds functions max words, save & exit
            if len(positions) > 1:                                          # if more than 1 position
                s = replace_all_occurences_forward(word,sub[0],sub[1],pos)  # replace every occurence from current pos forward
                substituted_passwords.add(s)
                if len(substituted_passwords) > max_words_generated and max_words_generated != 0:   
                    return substituted_passwords                            # if i exceeds functions max words, save & exit

            temp_substituted_passwords = substituted_passwords.copy()       # create a copy of current substituted words set
            for item in temp_substituted_passwords:                         # for each item in substituted_passwords before forloop began
                substituted_passwords.add(put_char_in_pos(sub,pos,item))    # apply this substitution and add to substituted passwords
                if len(substituted_passwords) > max_words_generated and max_words_generated != 0:   
                    return substituted_passwords                            # if i exceeds functions max words, save & exit
            
    return substituted_passwords

def remove_substitution(word):
    possible_words = set()

    s = word.replace('4','a')
    s = s.replace('@','a')
    s = s.replace('3','e')
    s = s.replace('€','e')
    s = s.replace('9','g')
    s = s.replace('!','i')
    s = s.replace('0','o')
    s = s.replace('$','s')
    s = s.replace('7','t')
    s = s.replace('2','z')
    s = s.replace('6','b')
    possible_words.add(s)
    s = s.replace('6','g')
    possible_words.add(s)
    s = s.replace('1','i')
    possible_words.add(s)
    s = s.replace('1','l')
    possible_words.add(s)
    s = s.replace('5','s')
    possible_words.add(s)
    s = s.replace('5','z')
    possible_words.add(s)

    return possible_words

def iterate_num_at_start_of_string(s):
    i = 0
    generated_pws = set()
    while i < 10:
        if s[0] != i:                   # finds number
            s = str(i) + s[1:]          # adds i to the start of the string
            generated_pws.add(s)
            i += 1

    return generated_pws        

def iterate_num_at_end_of_string(s):
    i = 0
    length = len(s)
    generated_pws = set()
    while i < 10:
        if s[0] != i:                       # finds number
            s = str(i) + s[:length]         # adds i to the end of the string
            generated_pws.add(s)
            i += 1
    
    return generated_pws

def add_most_popular_numbers(password,max_words_generated):
    generated_pws = set()
    print("Adding possible passwords with numbers...")
    with open("number_occurences.csv") as f:
        for line in f:
            for pw in possible_passwords:
                if re.match(r'(^\d[a-zA-Z])',pw):           # if password starts with just 1 number
                    for s in generated_pws:
                        generated_pws.union(iterate_num_at_start_of_string(s))

                if re.match(r'([a-zA-Z]\d$)',pw):           # if password ends with just 1 number
                    for s in generated_pws:
                        generated_pws.union(iterate_num_at_end_of_string(s))
                
                num = line.split(',')[0]                # extract number from most common numbers
                s = re.sub(r'^\d+',r'',pw)              # remove numbers from start of string
                s = re.sub(r'\d+$',r'',pw)              # remove numbers from end of string
                generated_pws.add(str(num) + s)
                generated_pws.add(s + str(num))         # append most popular numbers before and after password

                if len(generated_pws) >= max_words_generated and max_words_generated != 0:
                    return generated_pws

    return generated_pws 

def query_model(word):
    num_of_words = 5
    results = set()
    most_similar = []
    global model
    global model_path

    if model == None:               # if model is not initialised
        print("Loading Natural Language Processing Model...")
        try:
            start = time()
            nlp_model = w2v.load(model_path)
            print("Model Loaded Successfully! Took " + str(round(time()-start,2)) + " seconds.")
        except FileNotFoundError:
            print("Error: Model does not exist in path. Exiting...")
            exit()
        except ValueError:
            print("Path is not a valid model. Perhaps it is corrupt? Exiting...")
            exit()

    word = word.lower()                 # convert word to lowercase

    if word not in stopwords:                                   # only queries the model if word is not a stopword
        try:
            print("Querying model for: " + word)
            most_similar = nlp_model.wv.most_similar(word, topn=num_of_words)
        except KeyError:                                        # if word is not found in model
            word_found = False
            for possible_word in remove_substitution(word):     # attempt to remove any char substitution
                try:                                            # attempt to query the model again
                    most_similar = nlp_model.wv.most_similar(possible_word, topn=num_of_words)
                except KeyError:                                # if result not found, program will skip to next possible word
                    continue
                    
                word_found = True                               # becomes true if exception does not occur
                
            if word_found == False:
                print(word + " - Could not find result for this word in NLP model. This word will be skipped") 

    for item in most_similar:
        if item[1] > 0.7:                                      # if likeness > 0.7
            results.add(item[0])

    return results

def print_settings():
    global has_numbers
    global has_special_chars
    global use_nlp
    global max_length
    global min_length

    print("Natural Language Passwords - by Zack Anderson (1602117@uad.ac.uk)")
    print("Generating passwords using the following settings:")
    if has_numbers:
        print("     + Numbers")
    if has_special_chars:
        print("     + Special Characters")
    if use_nlp:
        print("     + Use Natural Language Processing")
    
    if max_length != 0:
        print("     + Length: " + str(min_length) + "-" + str(max_length) + " characters")
    else:
        print("     + Length: " + str(min_length) + "+ characters")
    if max_passwords != 0:
        print("     + Max Passwords: " + str(max_passwords))

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: " + str(argv[0]) + " [PASSWORD]")
        print("Seperate words in passphrases with ','")
        print("Flags (Place flags after password):\n"+
        "   -o=OUTPUT FILE (Default = current directory, [PASSWORD].txt)\n" +
        "   -min-length=MIN LENGTH (Default = 0)\n" +
        "   -max-length=MAX LENGTH (Default = unlimited)\n" +
        "   -max-passwords=MAX WORDS GENERATED (Default = unlimited)\n"
        "   -no-numbers\n" +
        "   -no-special-chars\n" +
        "   -no-nlp\n" +
        "   -model-path=PATH TO CUSTOM MODEL (Default = " + model_path + ")")
        exit()

    pw = str(argv[1]).strip()
    outpath = pw + '.txt'               # default outpath is [inputted password].txt in current directory"

    for arg in argv:
        if '-o=' in arg:
            outpath = arg.split('=')[-1]
        elif '-min-length=' in arg:
            try:
                min_length = int(''.join(arg.split('=')[-1]))
            except ValueError:
                print(arg + " - value not convertible to integer")
                exit()
        elif '-max-length=' in arg:
            try:
                max_length = int(''.join(arg.split('=')[-1]))
            except ValueError:
                print(arg + " - value not convertible to integer")
                exit()
        elif '-max-passwords=' in arg:
            try:
                max_passwords = int(''.join(arg.split('=')[-1]))
            except ValueError:
                print(arg + " - value not convertible to integer")
                exit()
        elif '-no-numbers' in arg:
            has_numbers = False
        elif '-no-special-chars' in arg:
            has_special_chars = False
        elif '-no-nlp' in arg:
            use_nlp = False
        elif 'model-path=' in arg:
            model_path = arg.split('=')[-1]

    passphrase = pw.split(',')                      # split passphrase into individual words
    pw = pw.replace(',','')                         # remove char to split passphrase 
    stopwords = set(stopwords.words('english'))

    print(ascii_art)
    print_settings()

    if has_numbers:
        append_to_set(add_most_popular_numbers(pw,(max_passwords/4)))

    append_to_set(char_substitution(pw,(max_passwords/4)))        

    if use_nlp:
        for word in passphrase:
            if max_passwords != 0:
                max_words = ((max_passwords - len(possible_passwords))/(len(passphrase)*5))
            else:
                max_words = 0
            for item in query_model(word):
                append_string_to_set(pw.replace(word,item))
                if len(item) > min_length:
                    append_to_set(char_substitution(pw.replace(word,item),max_words))
                else:
                    print(item + " - Word not longer than min length, skipping char substitution.")      
    
    print('Generated ' + str(len(possible_passwords)) + ' possible passwords using specified requirements.')

    try:
        outfile = open(outpath,'w+')
    except FileNotFoundError:
        print("Error: " + outpath + " - Directory does not exist, unable to save in this location.\nSaving in current location")
        outpath = outpath.split('/')[-1]   # for linux
        outpath = outpath.split('\\')[-1]  # for windows
        outfile = open(outpath,'w+')

    print("Saving as " + outpath)

    for possible_password in possible_passwords:
        outfile.write(str(possible_password) + '\n')
    
    outfile.close()