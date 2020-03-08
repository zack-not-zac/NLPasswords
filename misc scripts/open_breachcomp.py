def check_word(line, line_size, allowed_chars):
    valid_char = 0
    counter = 0
    word = list(line)                                               #convert the string into a list of chars
    print(word)
    for item in word:
        counter += 1
        if item in allowed_chars:
            valid_char += 1                                     #if the any character in the list is in the word, add 1 to valid_char
       
        if valid_char == line_size and counter == line_size:    #if end of word is reached and every character is valid, return true
            return True
        elif counter == line_size and valid_char != line_size:
            return False                                        #if it is invalid, return false

#alphabet = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h"
#    ,"I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y"
#    ,"Z","z"]
alphabet = ["h","i"]
numbers = ["0","1","2","3","4","5","6","7","8","9"]
special_chars = ["/","\'","\"","!","£","$","€","%","^","&","*","(",")","[","]","{","}","#","~","@"," ",":",";","?",".",",",">","<",
    "`","¬","\\","_","-","=","+"]

allowed_chars = alphabet + numbers + special_chars

word = input("enter word\n")
length = len(word)
print(word)
if check_word(word, length, allowed_chars) == True:
    print("valid")
else:
    print("invalid")