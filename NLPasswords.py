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
    if max_words == 0:
        max_words = 1500            # max number of words that can be added by 1 function
    items_added = 0
    global possible_passwords
    for item in s:
        if item != None:
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

                if items_added >= max_words:
                    if not unlimited_passwords:
                        return items_added # returns items_added if function generated more than max_words
                    else:
                        return 0

    if not unlimited_passwords:
        return items_added
    else:
        return 0

def append_string_to_list(s):
    if s != None:
        if s not in possible_passwords and s != pw:
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

def add_common_startend_chars(pw):
    ret = []
    for char in ['@','#','!','£','$','%','^','&','*','?','%']:# common typeable special chars used to meet password rules (based on https://github.com/danielmiessler/SecLists/blob/master/Passwords/Permutations/1337speak.txt)
        ret.append(char + pw)           # add char before
        ret.append(pw + char)           # add char after
    
    return ret

def char_substitution(word):
    substituted_passwords = list()
    max_items = None
    chars = {       # dictionary for char substitutions (https://code.sololearn.com/ceEeO2m4wGBG/#py)
        "a":"4,@",
        "b":"6,8",
        "e":"3",
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

    if len(word) >  16:
        max_items = 2000                                                    # max items that can be generated if word is over 16 chars

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

            if max_items != None and len(substituted_passwords) > max_items:
                return substituted_passwords

    return substituted_passwords

def remove_substitution(word,removeall=False):
    possible_words = list()
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
    
    if removeall:
        temp = word
        saved = []
        for char in temp:
            if chars.get(char.lower()) != None:
                subs = chars.get(char.lower()).split(',')
                if len(subs) > 1:
                    saved.append((char,subs))
                else:
                    temp = temp.replace(char,subs[0])

        if saved != None:
            templist = []
            templist.append(temp)
            for sub in saved:
                for char in sub[1]:
                    copy = templist.copy()
                    for item in copy:
                        if temp.replace(sub[0],char) not in templist:
                            templist.append(temp.replace(sub[0],char))

            for item in templist:
                if re.search(r'\d+',item) == None:
                    possible_words.append(item)   
        else:
            possible_words.append(temp)         

    for char in word:                                                       # for each character in password
        if chars.get(char.lower()) != None:                                 # if a substitution exists
            for char_substitute in chars.get(char.lower()).split(','):      # get all substitutions
                substitutions.add((char.lower(),char_substitute))
    for sub in substitutions:
        positions = [x for x,v in enumerate(word) if v.lower() == sub[0]]   # get all positions char (v) exists
        for pos in positions:                                               # for each position
            possible_words.append(put_char_in_pos(sub,pos,word))               # swap chars and add to list
            if len(positions) > 1:                                          # if more than 1 position
                s = replace_all_occurences_forward(word,sub[0],sub[1],pos)  # replace every occurence from current pos forward
                possible_words.append(s)

            temp_possible_words = possible_words.copy()              # create a copy of current substituted words set
            for item in temp_possible_words:                         # for each item in possible_words before forloop began
                possible_words.append(put_char_in_pos(sub,pos,item))    # apply this substitution and add to substituted passwords

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

def swap_startend_nums(pw):
    if re.search(r'[\d\W]+$',pw) != None and re.search(r'^[\d\W]+',pw) != None:
        startspan = re.search(r'^[\d\W]+',pw).span()[1]
        endspan = re.search(r'[\d\W]+$',pw).span()[0]
        start = pw[:startspan]
        end = pw[endspan:]
        word = pw[startspan:endspan]
        return end + word + start           # swap start and end chars/nums
    elif re.search(r'^[\d\W]+',pw) != None: # if word starts with numbers or special chars
        obj = re.search(r'^[\d\W]+',pw)     # get search object
        end = obj.span()[1]                 # get span of match
        num = pw[:end]                      # get starting nums or chars
        word = pw[end:]                     # strip from word
        return word + num                   # add numbers or chars to end of password and add to list
    elif re.search(r'[\d\W]+$',pw) != None: # if password ends with numbers or special chars
        obj = re.search(r'[\d\W]+$',pw)     # get search object
        start = obj.span()[0]               # get span of match
        num = pw[start:]                    # get ending nums or chars
        word = pw[:start]                   # strip from word
        return num + word                   # add numbers or chars to start of password and add to list

def add_most_popular_numbers(pw,top=0,is_char_sub=False):
    generated_pws = list()
    if not is_char_sub:
        if re.search(r'^\d[a-zA-Z]+',pw) != None:# if password starts with just 1 number
            generated_pws+=iterate_num_at_start_of_string(pw)

        if re.search(r'[a-zA-Z]+\d$',pw) != None:# if password ends with just 1 number
            generated_pws+=iterate_num_at_end_of_string(pw)
        pw = remove_nums_before_s(pw)                        # remove numbers from start of string
        pw = remove_nums_after_s(pw)                         # remove numbers from end of string

    i = 1

    with open("number_occurences.csv") as f:
        for line in f:
            num = int(line.split(',')[0].strip())       # extract number from most common numbers
            generated_pws.append(str(num) + pw)
            generated_pws.append(pw + str(num))          # append most popular numbers before and after password
            i += 1
            if i >= top and top != 0:
                return generated_pws

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
    s = remove_nums_after_s(word)
    s = remove_nums_before_s(s)

    if s not in stopwords:                                   # only queries the model if word is not a stopword
        try:
            print("Querying model for: " + s)
            most_similar = model.wv.most_similar(s, topn=num_of_words)
        except KeyError:
            word_found = False
            for ret_word in remove_substitution(word,removeall=True):
                try:
                    most_similar = model.wv.most_similar(ret_word,topn=num_of_words)
                    word_found = True                               # becomes true if exception does not occur
                    print("Word stripped to: " + ret_word)
                    break
                except KeyError:
                    try:
                        ret_word = remove_nums_after_s(ret_word)
                        ret_word = remove_nums_before_s(ret_word)
                        most_similar = model.wv.most_similar(ret_word,topn=num_of_words)
                        word_found = True
                        print("Word stripped to: " + ret_word)
                        break
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
        s = remove_nums_before_s(s)
        s = remove_nums_after_s(s)
        s = s.lower()
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
    global unlimited_passwords
    ret = set()
    temp_phrase = str()
    for word in phrase:
        capitalise_first_char(word)
        temp_phrase += word   # appends capitalised letter word to temp_phrase
    ret.add(temp_phrase)
    ret.add(''.join(phrase).upper())         # add full capitalisation
    ret.add(''.join(phrase).lower())         # add full lowercase

    if try_all_capitalisation or unlimited_passwords:
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
    outpath = pw.replace(',','') + '.txt'               # default outpath is [inputted password].txt in current directory"
    
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
    words_per_func = int(max_passwords/num_of_funcs)

    print("Adding capitalisation to current password...")
    max_passwords -= append_to_list(capitalise_letters(passphrase),words_per_func)
    print("Switching any starting or ending numbers or special characters...")
    max_passwords -= append_string_to_list(swap_startend_nums(pw))
    # sets max_passwords to how many spaces are left
    
    if has_numbers:
        print("Adding popular numbers to original password...")
        max_passwords -= append_to_list(add_most_popular_numbers(pw),words_per_func)

    print("Removing any substitution from original password...")
    if unlimited_passwords or must_have_special_chars:  
        max_passwords -= append_to_list(add_common_startend_chars(pw),words_per_func)
    max_passwords -= append_to_list(remove_substitution(pw),words_per_func)
    print("Performing character substitution on original password...")
    char_substitutes = char_substitution(pw)
    char_substitutes_with_num = []

    if has_numbers:
        print("Adding popular numbers to character substituted passwords...")
        for s in char_substitutes:
            char_substitutes_with_num += add_most_popular_numbers(s,top=5,is_char_sub=True)      # adds top5 most popular passwords

    max_passwords -= append_to_list(char_substitutes,words_per_func)
    max_passwords -= append_to_list(char_substitutes_with_num,words_per_func)

    if use_nlp:
        startnum = None
        endnum = None
        result = 0
        if len(passphrase) > 1:
            if not unlimited_passwords:
                max_words = int(max_passwords/((len(passphrase)+1)*num_of_words))
            else:
                max_words = 0
            
            most_similar = query_model_list(passphrase)
            for item in most_similar:
                for i,passphrase_word in enumerate(passphrase):
                    if passphrase_word.lower() not in stopwords:
                        temp = passphrase.copy()
                        temp[i] = item[0]
                        max_passwords -= append_string_to_list(''.join(temp))

        else:
            if not unlimited_passwords:
                max_words = int(max_passwords/((len(passphrase))*num_of_words))
            else:
                max_words = 0
                
        for word in passphrase:
            startnum = None
            endnum = None
            startend_nums = strip_startend_nums_from_s(word)# retreive any numbers at start or end
            if len(startend_nums) != 0:                 # if pw has numbers at start or end
                for num in startend_nums:               # for each value
                    if num[0] =='start':                # if num is start number
                        startnum = num[1]               # gets start numbers from pw
                    elif num[0] == 'end':               # if num is end number
                        endnum = num[1]                 # gets end numbers from pw

            for item in query_model(word):
                count = 0                                   # ensures each word does not use more than it was dedicated in wordlist
                tempword = str()
                
                popular_nums = add_most_popular_numbers(item)# add most popular numbers to the item
                charsub = char_substitution(item)           # get char substitution for item

                tempword += item

                if startnum != None:
                    tempword = str(startnum) + tempword           # appends startnum to item if exists

                if endnum != None:
                    tempword += str(endnum)             # appends endnum to item if exists

                result = append_string_to_list(pw.replace(word,tempword))# adds to set
                max_passwords -= result
                count += result
                if count > max_words and max_words != 0:
                    continue
                
                old = tempword
                for sub in charsub:
                    result= append_string_to_list(sub)      # adds sub to list
                    max_passwords -= result
                    count += result
                    tempword = tempword.replace(item,sub)
                    result = append_string_to_list(tempword) # adds sub with start/endnums to set
                    tempword = old                           # changes tempword back to original for replace()
                    count += result
                    max_passwords -= result
                    if max_passwords < 0:
                        break
                    elif count > max_words and max_words != 0:
                        break

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
