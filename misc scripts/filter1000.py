from os import path,remove
import re

if __name__ == "__main__":
    invalid_words = []
    i = 0
    maxwords = 1000
    alphabet = {"A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h"
    ,"I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y"
    ,"Z","z"}
    numbers = {"0","1","2","3","4","5","6","7","8","9"}
    special_chars = {"/","\'","\"","!","£","$","€","%","^","&","*","(",")","[","]","{","}","#","~","@"," ",":",";","?",".",",",">","<","`","¬","\\","_","-","=","+"}

    allowed_chars = alphabet.union(numbers).union(special_chars)                      #defines all chars allowed to be used (see above)

    infile = "/home/zack/Desktop/Hons Project/breachcompilation.txt"
    outfile = "/home/zack/Desktop/Hons Project/breachcomp/breachcompfirst1000_filtered.txt"

    if path.exists(outfile):
        remove(outfile)

    output = open(outfile, "a+")

    with open(infile, "r") as f:
        for line in f:
            valid_chars = 0
            line = line.strip()
            chars = list(line)
            for char in chars:
                if char in allowed_chars:
                    valid_chars += 1
            
            if valid_chars == len(chars):
                if re.match(r"([a-fA-F\d]{32})",line) or re.match(r"([a-fA-F\d]{20})",line) or line == "":
                    invalid_words.append(line)
                else:
                    output.write(line + "\n")
                    i += 1
            else:
                invalid_words.append(line)

            if i == maxwords:
                output.close()
                print(invalid_words)
                exit()