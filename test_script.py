from os import chdir
import subprocess

chdir('/home/zack/Desktop/Hons-Project')

testfile = open('test passwords.txt', 'r').readlines()
testpasswords = []

outfile = open('testresults.csv', 'w+')

if __name__ == '__main__':
    for line in testfile:
        line = line.strip()
        if len(line) > 0:
            if not line.startswith('-'):
                testpasswords.append(tuple(line.split(':')))

    for testset in testpasswords:
        command = '/home/zack/Desktop/Hons-Project/create_wordlist.py ' + str(testset[0])
        _ = subprocess.call(command,shell=True)

        # test with custom wordlist
        pws = open(testset[0] + '.txt', 'r').readlines()
        wordlist = 'custom'
        for attempts, generated_pw in enumerate(pws):
            found = False
            if generated_pw == testset[1]:
                outfile.write(wordlist + ',' +
                              testset[0] + ',' + testset[1] + ',' + attempts + '\n')
            elif attempts == len(pws) and found == False:
                outfile.write(wordlist + ',' + testset[0] + ',-,NF\n')

        # test with rockyou.txt
        wordlist = 'rockyou'
        with open('/home/zack/Downloads/rockyou.txt') as f:
            for pw in f:
                found = False
                if pw == testset[1]:
                    outfile.write(wordlist + ',' +
                                  testset[0] + ',' + testset[1] + ',' + attempts + '\n')

            if found == False:
                outfile.write(wordlist + ',' + testset[0] + ',-,NF\n')