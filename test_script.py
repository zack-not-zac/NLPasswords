from os import chdir
import subprocess

def main():
    chdir('/home/zack/Desktop/Hons-Project')

    testfile = open('test passwords.txt', 'r').readlines()
    testpasswords = []

    outfile = open('testresults.csv', 'w+')

    for line in testfile:
        line = line.strip()
        if len(line) > 0:
            if not line.startswith('-'):
                testpasswords.append(tuple(line.split(':')))

    for testset in testpasswords:
        print('Testing ' + testset[0])
        command = '/home/zack/Desktop/Hons-Project/create_wordlist.py ' + str(testset[0])
        subprocess.call(command,shell=True,stdout=subprocess.DEVNULL)

        # test with custom wordlist
        pws = open(testset[0] + '.txt', 'r').readlines()
        wordlist = 'custom'
        for attempts, generated_pw in enumerate(pws):
            found = False
            generated_pw = generated_pw.strip()
            if generated_pw == testset[1]:
                outfile.write(wordlist + ',' +
                              testset[0] + ',' + testset[1] + ',' + str(attempts) + '\n')
            elif attempts == len(pws)-1 and found == False:
                outfile.write(wordlist + ',' + testset[0] + ',-,NF\n')

        # test with rockyou.txt
        wordlist = 'rockyou'
        with open('/home/zack/Downloads/rockyou.txt','r',encoding='ISO-8859-1') as f:
            for pw in f:
                pw = pw.strip()
                found = False
                if pw == testset[1]:
                    outfile.write(wordlist + ',' +
                                  testset[0] + ',' + testset[1] + ',' + str(attempts) + '\n')

            if found == False:
                outfile.write(wordlist + ',' + testset[0] + ',-,NF\n')
    
    outfile.close()

if __name__ == '__main__':
    main()