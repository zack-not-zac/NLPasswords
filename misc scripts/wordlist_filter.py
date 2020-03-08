#!/usr/bin/env python3

import os
import threading
import time
import sys

invalid_output = None       # empty var for invalid words output file
output = None               # empty var for output file
valid_count = 0             # num of valid words
lines_processed = 0         # num of lines processed
finished = False            # variable to tell progress thread when program has finished

def check_progress():
    global lines_processed      # global variable for num of lines processed
    global valid_count          # global variable for num of valid entries
    global finished             # tells the thread if the program is finished
    start = time.time()         # time the program started at
    print_delay = time.time()   #tells the loop how long it has been since it last printed
    
    while not finished:
        if (time.time() - print_delay > 5):
            print(str(lines_processed) + " lines processed, " + str(valid_count) + " valid entries. " + str(round(time.time() - start, 3))  + "s elapsed")
            print_delay = time.time()       #updates the time so the function does not print for another 5 seconds
    
    print("Finished! " + str(lines_processed) + " lines processed, " + str(valid_count) + " valid entries. Took " + str(round(time.time() - start, 3)) + " seconds")
    exit()

def check_output_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)        #removes the file if it exists before running the script
        output = open(filepath, "a+")
    else:
        output = open(filepath, "a+")
    return output

def get_valid_chars():
    alphabet = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h"
    ,"I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y"
    ,"Z","z"]
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    special_chars = ["/","\'","\"","!","£","$","€","%","^","&","*","(",")","[","]","{","}","#","~","@"," ",":",";","?",".",",",">","<",
    "`","¬","\\","_","-","=","+"]

    allowed_chars = alphabet + numbers + special_chars                      # defines all chars allowed to be used (see above)
    return allowed_chars

def check_word(line, line_size, allowed_chars):
    valid_char = 0
    counter = 0
    word = list(line)                                               #convert the string into a list of chars
    for item in word:
        counter += 1
        if item in allowed_chars:
            valid_char += 1                                         #if the character is in allowed_chars, add 1 to valid_char
       
        if valid_char == line_size and counter == line_size:        #if end of word is reached and every character is valid, return true
            return True
        elif counter == line_size and valid_char != line_size:
            return False                                            #if it is invalid, return false

def checklines(lines):
    global invalid_output
    global output
    global valid_count
    global lines_processed
    
    valid_words = []                    # list to store valid words
    invalid_words = []                  # list to store invalid words
    allowed_chars = get_valid_chars()   # list of valid characters

    for line in lines:
        line_size = len(line)
        lines_processed += 1
        if line_size > 1:           #checks if the password is longer than 1 char long
            if check_word(line, line_size, allowed_chars):
                valid_words.append(line)
            else:
                invalid_words.append(line)
                            
        else:  
            invalid_words.append(line)
    
    mutex = threading.Lock()
    with mutex:
        valid_count += len(valid_words)             # adds the number of valid words to the valid_count var

    for i in valid_words:
        output.write(i + "\n")                      # write valid words to file
    for i in invalid_words:
        invalid_output.write(i + "\n")              # write invalid words to file

def read_file(infile, worker_threads):
    global finished
    global lines_processed
    wordlist = []           # an empty list to read the text file into
    i = 0                   # iterator
    split = 1000000         # number of lines each thread should handle at a time
    threads = []            # list of thread objects
    with open(infile) as f:
        for line in f:
            line = line.strip()     #strip newline chars
            line = str(line)        #convert line to string from bytes
            wordlist.append(line)
            i += 1

            lines_processed += 1

            if i > split:
                # while threading.activeCount() >= worker_threads + 8:              FOR DEBUGGING
                #     print(threading.enumerate())
                #     time.sleep(1)                                                           # ensures the max thread count is not exceeded
                
                while threading.activeCount() >= worker_threads:
                    print(threading.enumerate())
                    time.sleep(1)                                                           # ensures the max thread count is not exceeded
                
                threads.append(threading.Thread(target=checklines, args=(wordlist,)))       # creates a new thread to process the wordlist
                threads[-1].start()                                                         # gets the element at the end of the list, starts the new thread
                wordlist.clear()                                                            # clears the wordlist for the next thread
                i = 0                                                                       # resets iterator
    
    for i in threads:
        i.join()

    finished = True

if __name__ == "__main__":
    worker_threads = 4                          # number of threads
    outfile = "./valid_words.txt"               # path and name of output file
    infile = "./breachcompilation.txt"          # path and name of input file
    invalid_outfile = "./invalid_words.txt"     # filepath for invalid words

    if len(sys.argv) != 5:
        print("Usage: " + str(sys.argv[0] + " [input file] [output file] [invalid strings output file] [number of threads]"))
        exit()
    else:
        infile = str(sys.argv[1])
        outfile = str(sys.argv[2])
        invalid_outfile = str(sys.argv[3])
        worker_threads = int(sys.argv[4])

    if not os.access(infile, os.R_OK):
        print("Error reading input file...")
        exit()

    output = check_output_file(outfile)
    invalid_output = check_output_file(invalid_outfile)

    progress_thread = threading.Thread(target=check_progress)
    progress_thread.start()                                                 # thread to print progress of the program

    read_file(infile,worker_threads)                                        # starts to read the file
