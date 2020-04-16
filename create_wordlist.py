#!/usr/bin/env python3

from gensim.models import Word2Vec as w2v
from nltk.corpus import stopwords
from sys import argv
import re
from time import time

total_time = time()                 # starts a timer
num_of_words = 5                    # num of words returned by the NLP model
possible_passwords = list()         # a list for generated pws
has_numbers = True                  # numbers flag for passwords
has_special_chars = True            # special chars for passwords
use_nlp = True                      # use NLP model
max_length = 0                      # max password length
min_length = 0                      # min password length
model = None                        # variable for storing NLP model
max_passwords = 0                   # max passwords outputted by the program
unlimited_passwords = True          # unlimited passwords allowed by the program
try_all_capitalisation = False      # specify if the script should generate all possible capitalisations
must_have_numbers = False           # if generated passwords must have numbers
must_have_special_chars = False     # if generated passwords must have special chars
pw = ''                             # var to hold password
model_path = "models/w2v/w2v_wikipedia_and_reddit_comments.model"
# ascii art generated with https://manytools.org/hacker-tools/ascii-banner/
ascii_art = r""" __   __     __         ______   ______     ______     ______     __     __     ______     ______     _____     ______    
/\ "-.\ \   /\ \       /\  == \ /\  __ \   /\  ___\   /\  ___\   /\ \  _ \ \   /\  __ \   /\  == \   /\  __-.  /\  ___\   
\ \ \-.  \  \ \ \____  \ \  _-/ \ \  __ \  \ \___  \  \ \___  \  \ \ \/ ".\ \  \ \ \/\ \  \ \  __<   \ \ \/\ \ \ \___  \  
 \ \_\\"\_\  \ \_____\  \ \_\    \ \_\ \_\  \/\_____\  \/\_____\  \ \__/".~\_\  \ \_____\  \ \_\ \_\  \ \____-  \/\_____\ 
  \/_/ \/_/   \/_____/   \/_/     \/_/\/_/   \/_____/   \/_____/   \/_/   \/_/   \/_____/   \/_/ /_/   \/____/   \/_____/ 
                                                                                                                          """

def replace_all_occurences_forward(pw,char,sub,pos):
    s = pw[pos:]                                # clips string from pos forward
    s_before = pw[:pos]                         # takes the chars from before pos
    s = s_before + s.replace(char,sub)          # stitches string back together with all substitutions after pos implemented
    return s

def append_to_list(s,max_words):
    items_added = 0
    global possible_passwords
    for i,item in enumerate(s):
        if item not in possible_passwords and item != pw:
            if len(item) <= max_length or max_length == 0 and len(item) >= min_length:  # if the string is less than max length or more than min length, max length = 0 (no limit)
                if not has_numbers and re.search(r'\d',item) ==  None:             # if pw shouldn't have numbers and doesn't
                    if not has_special_chars and re.search(r'\W',item) == None:
                        possible_passwords.append(item)
                        items_added += 1
                elif not has_special_chars and re.search(r'\W',item) == None:     # if pw shouldn't have special chars and doesnt
                    possible_passwords.append(item)
                    items_added += 1

                if must_have_numbers and re.search(r'\d',item) != None:
                    if must_have_special_chars and re.search(r'\W',item) != None:
                        possible_passwords.append(item)
                        items_added += 1
                elif must_have_special_chars and re.search(r'\W',item) != None:
                    possible_passwords.append(item)
                    items_added += 1
                else:
                    possible_passwords.append(item)
                    items_added += 1

            if i >= max_words and not unlimited_passwords:
                return items_added # returns items_added if function generated more than max_words

    if not unlimited_passwords:
        return items_added
    else:
        return 0

def append_string_to_list(s):
    if s not in possible_passwords and item != pw:
        if len(s) <= max_length or max_length == 0 and len(s) >= min_length:  # if the string is less than max length or more than min length, max length = 0 (no limit)
            if not has_numbers and re.search(r'\d',s) ==  None:             # if pw shouldn't have numbers and doesn't
                if not has_special_chars and re.search(r'\W',s) == None:
                    possible_passwords.append(s)
                    if not unlimited_passwords:
                        return 1
                    else:
                        return 0
            elif not has_special_chars and re.search(r'\W',s) == None:     # if pw shouldn't have special chars and doesnt
                    possible_passwords.append(s)
                    if not unlimited_passwords:
                        return 1
                    else:
                        return 0

            if must_have_numbers and re.search(r'\d',s) != None:
                if must_have_special_chars and re.search(r'\W',s) != None:
                    possible_passwords.append(s)
                    if not unlimited_passwords:
                        return 1
                    else:
                        return 0
            elif must_have_special_chars and re.search(r'\W',s) != None:
                possible_passwords.append(s)
                if not unlimited_passwords:
                    return 1
                else:
                    return 0
            else:
                possible_passwords.append(s)
                if not unlimited_passwords:
                    return 1
                else:
                    return 0

    return 0

def put_char_in_pos(sub,pos,pw):
    temp = list(pw)                             # convert pw into list
    temp[pos] = sub[1]                          # change char to substitute
    s = ''.join(temp)                           # join list back into str
    return s

def char_substitution(word):
    substituted_passwords = list()
    chars = {       # dictionary for char substitutions (https://code.sololearn.com/ceEeO2m4wGBG/#py)
        "a":"4,@",
        "b":"6,8",
        "e":"3,€",
        "g":"6,9",
        "i":"1,!",
        "l":"1",
        "o":"0",
        "s":"5,$",
        "t":"7",
        "z":"2,5",
        "1":"!",
        "4":"@"}

    substitutions = set()
    if must_have_special_chars or unlimited_passwords:
        for char in ['@','#','!','£','$','%','^','&','*','?','%']:# common typeable special chars used to meet password rules (based on https://github.com/danielmiessler/SecLists/blob/master/Passwords/Permutations/1337speak.txt)
            substituted_passwords.append(char + word)           # add char before
            substituted_passwords.append(word + char)           # add char after
    for char in word:                                                       # for each character in password
        if chars.get(char.lower()) != None:                                 # if a substitution exists
            for char_substitute in chars.get(char.lower()).split(','):      # get all substitutions
                substitutions.add((char.lower(),char_substitute))
    for sub in substitutions:
        positions = [x for x,v in enumerate(word) if v.lower() == sub[0]]   # get all positions char (v) exists
        for pos in positions:                                               # for each position
            substituted_passwords.append(put_char_in_pos(sub,pos,word))     # swap chars and add to list
            if len(positions) > 1:                                          # if more than 1 position
                s = replace_all_occurences_forward(word,sub[0],sub[1],pos)  # replace every occurence from current pos forward
                substituted_passwords.append(s)

            temp_substituted_passwords = substituted_passwords.copy()       # create a copy of current substituted words set
            for item in temp_substituted_passwords:
                temp = put_char_in_pos(sub,pos,item)                        # for each item in substituted_passwords before forloop began
                if temp not in substituted_passwords:
                    substituted_passwords.append(temp)                      # apply this substitution and add to substituted passwords

    return substituted_passwords

def remove_substitution(word):
    possible_words = set()
    substitutions = set()

    chars = {
        "4":"a",
        "@":"a",
        "6":"b,g",
        "3":"e",
        "9":"g",
        "8":"b",
        "7":"t",
        "€":"e",
        "1":"l,i",
        "!":"i",
        "5":"s,z",
        "$":"s",
        "0":"o",
        "2":"z",
    }

    for char in word:                                                       # for each character in password
        if chars.get(char.lower()) != None:                                 # if a substitution exists
            for char_substitute in chars.get(char.lower()).split(','):      # get all substitutions
                substitutions.add((char.lower(),char_substitute))
    for sub in substitutions:
        positions = [x for x,v in enumerate(word) if v.lower() == sub[0]]   # get all positions char (v) exists
        for pos in positions:                                               # for each position
            possible_words.add(put_char_in_pos(sub,pos,word))               # swap chars and add to list
            if len(positions) > 1:                                          # if more than 1 position
                s = replace_all_occurences_forward(word,sub[0],sub[1],pos)  # replace every occurence from current pos forward
                possible_words.add(s)

            temp_possible_words = possible_words.copy()              # create a copy of current substituted words set
            for item in temp_possible_words:                         # for each item in possible_words before forloop began
                possible_words.add(put_char_in_pos(sub,pos,item))    # apply this substitution and add to substituted passwords

    return possible_words

def iterate_num_at_start_of_string(s):
    i = 0
    generated_pws = list()
    subs = char_substitution(s[1:])
    while i < 10:
        if s[0] != i:                   # finds number
            temp = str(i) + s[1:]          # adds i to the start of the string
            generated_pws.append(temp)
            for sub in subs:
                generated_pws.append(str(i) + sub)
            i += 1

    return generated_pws

def iterate_num_at_end_of_string(s):
    i = 0
    generated_pws = list()
    subs = char_substitution(s[:-1])
    while i < 10:
        if s[-1] != i:                      # finds number
            temp = s[:-1] + str(i)             # adds i to the end of the string
            generated_pws.append(temp)
            for sub in subs:
                if sub+str(i) not in generated_pws:
                    generated_pws.append(sub + str(i))         
            i += 1

    return generated_pws

def add_most_popular_numbers(pw):
    generated_pws = list()
    if re.search(r'^\d[a-zA-Z]+',pw) != None:# if password starts with just 1 number
        generated_pws+=iterate_num_at_start_of_string(pw)

    if re.search(r'[a-zA-Z]+\d$',pw) != None:# if password ends with just 1 number
        generated_pws+=iterate_num_at_end_of_string(pw)

    if re.search(r'^[\d\W]+',pw) != None:   # if word starts with numbers or special chars
        obj = re.search(r'^[\d\W]+',pw)     # get search object
        end = obj.span()[1]                 # get span of match
        num = pw[:end]                      # get starting nums or chars
        word = pw[end:]                     # strip from word
        generated_pws.append(word + num)    # add numbers or chars to end of password and add to list
    elif re.search(r'[\d\W]+$',pw) != None: # if password ends with numbers or special chars
        obj = re.search(r'[\d\W]+$',pw)     # get search object
        start = obj.span()[0]               # get span of match
        num = pw[start:]                    # get ending nums or chars
        word = pw[:start]                   # strip from word
        generated_pws.append(num + word)    # add numbers or chars to start of password and add to list


    s = remove_nums_before_s(pw)                        # remove numbers from start of string
    s = remove_nums_after_s(s)                          # remove numbers from end of string

    with open("number_occurences.csv") as f:
        for line in f:
            num = int(line.split(',')[0].strip())       # extract number from most common numbers
            generated_pws.append(str(num) + s)
            generated_pws.append(s + str(num))          # append most popular numbers before and after password

    return generated_pws

def remove_nums_before_s(s):        # removes nums or special chars at start of string
    return re.sub(r'^[\d\W]+',"",s)

def remove_nums_after_s(s):         # removes nums at end of string
    return re.sub(r'[\d\W]+$',"",s)

def capitalise_first_char(s):
    l = list(s)
    l[0] = l[0].upper()
    return ''.join(l)

def query_model(word):
    results = list()
    most_similar = list()
    global model
    global model_path
    global num_of_words
    global stopwords

    if list(word)[0].isupper():
        firstupper = True
    else:
        firstupper = False    

    if model == None:               # if model is not initialised
        print("Loading Natural Language Processing Model...")
        try:
            start = time()
            model = w2v.load(model_path)
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
            most_similar = model.wv.most_similar(word, topn=num_of_words)
        except KeyError:
            word_found = False
            possible_word = remove_nums_after_s(word)
            possible_word = remove_nums_before_s(possible_word)
            try:
                most_similar = model.wv.most_similar(possible_word,topn=num_of_words)
                word_found = True                               # becomes true if exception does not occur
                print("Word stripped to: " + possible_word)
            except KeyError:
                for ret_word in remove_substitution(word):
                    try:
                        most_similar = model.wv.most_similar(ret_word,topn=num_of_words)
                        word_found = True                               # becomes true if exception does not occur
                        print("Word stripped to: " + ret_word)
                    except KeyError:
                        try:
                            ret_word = remove_nums_after_s(ret_word)
                            ret_word = remove_nums_before_s(ret_word)
                            most_similar = model.wv.most_similar(ret_word,topn=num_of_words)
                            word_found = True
                            print("Word stripped to: " + ret_word)
                        except KeyError:
                            continue

            if word_found == False:
                print(word + " - Could not find result for this word in NLP model. This word will be skipped")

    for item in most_similar:
        if item[1] > 0.5:                                      # if likeness > 0.7
            if firstupper:
                results.append(capitalise_first_char(item[0]))
            else:
                results.append(item[0])

    return results

def query_model_list(l):
    most_similar = list()
    global model
    global model_path
    global num_of_words
    global stopwords
    query = list()

    if model == None:               # if model is not initialised
        print("Loading Natural Language Processing Model...")
        try:
            start = time()
            model = w2v.load(model_path)
            print("Model Loaded Successfully! Took " + str(round(time()-start,2)) + " seconds.")
        except FileNotFoundError:
            print("Error: Model does not exist in path. Exiting...")
            exit()
        except ValueError:
            print("Path is not a valid model. Perhaps it is corrupt? Exiting...")
            exit()
    
    for s in l:
        remove_nums_before_s(s)
        remove_nums_after_s(s)
        if s not in stopwords:
            query.append(s)

    try:
        most_similar = model.wv.most_similar(query,topn=num_of_words)
    except KeyError:
        for i,item in enumerate(query):
            for ret in remove_substitution(item):
                try:
                    model.wv.most_similar(ret,topn=1)
                    query[i] = ret
                except KeyError:
                    continue

    try:
        most_similar = model.wv.most_similar(query,topn=num_of_words)
    except KeyError:
        print('1 or more words in passphrase not in model. Unable to solve by removing character substitution, skipping...')
        return []
    
    return most_similar

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
    if not unlimited_passwords:
        print("     + Max Passwords: " + str(max_passwords))

def capitalise_letters(phrase):
    global try_all_capitalisation
    ret = set()
    temp_phrase = str()
    for word in phrase:
        s = list(word)              # split phrase into list of chars
        s[0] = s[0].upper()         # converts first letter to uppercase
        temp_phrase += ''.join(s)   # appends capitalised letter word to temp_phrase
    ret.add(temp_phrase)
    ret.add(''.join(phrase).upper())         # add full capitalisation
    ret.add(''.join(phrase).lower())         # add full lowercase

    if try_all_capitalisation:
        l=list(''.join(phrase))
        for x,char in enumerate(l):
            temp = l.copy()
            temp[x] = char.upper()      # capitalises current letter
            ret.add(''.join(temp))      # adds the string to ret
            for i,_ in enumerate(temp):
                copy = temp.copy()
                copy[i] = copy[i].upper()
                ret.add(''.join(copy))
            s1 = ''.join(phrase[x:])    # gets string before position x
            s2 = ''.join(phrase[:x])    # gets string after position x
            ret.add(s1 + s2.upper())    # capitalises string after pos
            ret.add(s1.upper() + s2)    # capitalises string before pos

    try:
        ret.remove(''.join(phrase))     # remove original phrase if it ended up in the list
    except KeyError:
        pass                            # ignore if original not found
    return ret

def strip_startend_nums_from_s(word):       # returns a list of 2 strings, nums before and nums after
    ret = list()                            # return list
    start_nums = re.search(r'^\d+',word)
    end_nums = re.search(r'\d+$',word)

    word = list(word)
    try:
        endspan = end_nums.span()
    except AttributeError:
        endspan = None                  # returns none if no nums found

    try:
        startspan = start_nums.span()
    except AttributeError:
        startspan = None                # returns none if no nums found

    if startspan != None:
        ret.append(('start',''.join(word[:startspan[1]])))
    if endspan != None:
        ret.append(('end',''.join(word[endspan[0]:])))

    return ret

if __name__ == "__main__":
    num_of_funcs = 6        # number of functions applied to password
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
        "   -model-path=PATH TO CUSTOM MODEL (Default = " + model_path + ")\n"
        "   -must-have-numbers\n"+
        "   -must-have-special-chars\n"+
        "   -try-all-capitalisation (will try every possible pattern using capitalisation)\n" +
        "   -num-of-words=[NUMBER OF WORDS TO BE RETURNED BY THE MODEL] (default = 5)")
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
                unlimited_passwords = False
            except ValueError:
                print(arg + " - value not convertible to integer")
                exit()
        elif '-no-numbers' in arg:
            has_numbers = False
        elif '-no-special-chars' in arg:
            has_special_chars = False
        elif '-no-nlp' in arg:
            use_nlp = False
            num_of_funcs -=1
        elif 'model-path=' in arg:
            model_path = arg.split('=')[-1]
        elif '-must-have-numbers' in arg:
            must_have_numbers = True
        elif '-must-have-special-chars' in arg:
            must_have_special_chars = True
        elif 'try-all-capitalisation' in arg:
            try_all_capitalisation = True
        elif '-num-of-words' in arg:
            try:
                num = int(arg.split('=')[-1])
            except ValueError:
                print(str(arg) + " - value not convertible to integer")
                exit()

    passphrase = pw.split(',')                      # split passphrase into individual words
    pw = pw.replace(',','')                         # remove char to split passphrase
    try:
        stopwords = set(stopwords.words('english'))
    except LookupError:
        from nltk import download
        download('stopwords')
        stopwords = set(stopwords.words('english'))

    print(ascii_art)
    print_settings()
    words_per_func = max_passwords/num_of_funcs

    print("Adding capitalisation to current password...")
    max_passwords -= append_to_list(capitalise_letters(passphrase),words_per_func)
    # sets max_passwords to how many spaces are left
    if has_numbers:
        print("Adding popular numbers to original password...")
        max_passwords -= append_to_list(add_most_popular_numbers(pw),(max_passwords/num_of_funcs))

    print("Removing any substitution from original password...")
    max_passwords -= append_to_list(remove_substitution(pw),(max_passwords/num_of_funcs))
    print("Performing character substitution on original password...")
    char_substitutes = char_substitution(pw)

    if has_numbers:
        print("Adding popular numbers to character substituted passwords...")
        for s in char_substitutes:
            char_substitutes_with_num = add_most_popular_numbers(s)

    max_passwords -= append_to_list(char_substitutes,(max_passwords/num_of_funcs))
    max_passwords -= append_to_list(char_substitutes_with_num,(max_passwords/num_of_funcs))

    if use_nlp:
        startnum = None
        endnum = None
        count = 0                                   # ensures each word does not use more than it was dedicated in wordlist
        result = 0
        if len(passphrase) > 1:
            if not unlimited_passwords:
                max_words = int(max_passwords/((len(passphrase)+1)*num_of_words))
            else:
                max_words = 0

            result = append_to_list(query_model_list(passphrase),max_words)
            max_passwords -= result
            count += result
        else:
            if not unlimited_passwords:
                max_words = int(max_passwords/((len(passphrase))*num_of_words))
            else:
                max_words = 0
                
        for word in passphrase:
            for item in query_model(word):
                tempword = str()
                startend_nums = strip_startend_nums_from_s(word)# retreive any numbers at start or end
                popular_nums = add_most_popular_numbers(item)# add most popular numbers to the item
                charsub = char_substitution(item)           # get char substitution for item
                if len(startend_nums) != 0:                 # if pw has numbers at start or end
                    for num in startend_nums:               # for each value
                        if num[0] =='start':                # if num is start number
                            startnum = num[1]               # gets start numbers from pw
                        elif num[0] == 'end':               # if num is end number
                            endnum = num[1]                 # gets end numbers from pw

                    if startnum != None:
                        tempword += str(startnum)           # appends startnum to item if exists

                    tempword += item

                    if endnum != None:
                        tempword += str(endnum)             # appends endnum to item if exists

                    result = append_string_to_list(tempword)# adds to set
                    max_passwords -= result
                    count += result
                    if count > max_words and max_words != 0:
                        continue

                    for sub in charsub:
                        result= append_string_to_list(sub)      # adds sub to set
                        max_passwords -= result
                        count += result
                        tempword = tempword.replace(item,sub)
                        result = append_string_to_list(tempword) # adds sub with start/endnums to set
                        count += result
                        max_passwords -= result
                        if max_passwords < 0:
                            break
                        elif count > max_words and max_words != 0:
                            break
                else:
                    result = append_string_to_list(pw.replace(word,item))
                    count += result
                    max_passwords -= result

                if max_passwords < 0:
                    break
                if len(item) > min_length:
                    if count < max_words or max_words == 0:
                        result = append_to_list(popular_nums,max_words)
                        count += result
                        max_passwords -= result
                        if max_passwords < 0:
                            break
                        elif count > max_words and max_words != 0:
                            continue
                else:
                    print(item + " - Word not longer than min length, skipping char substitution.")

    print('Generated ' + str(len(possible_passwords)) + ' possible passwords using specified requirements in ' + str(round(time()-total_time,2)) + ' seconds.')

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