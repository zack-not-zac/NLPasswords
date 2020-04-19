from os import chdir
import subprocess


def test_custom(old_password, new_password):
    ret = str()
    print('Testing ' + old_password)
    command = "/home/zack/Desktop/Hons-Project/NLPasswords.py '" + \
        str(old_password) + "'"
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

    # test with custom wordlist
    pws = open(old_password.replace(',', '') + '.txt', 'r').readlines()
    for attempts, generated_pw in enumerate(pws):
        found = False
        generated_pw = generated_pw.strip()
        if generated_pw == new_password:
            ret = str(attempts)
            found = True
            break
        elif attempts == len(pws)-1 and found == False:
            ret = 'NF'

    subprocess.call("rm '" + old_password.replace(',', '') + ".txt'",
                    shell=True, stdout=subprocess.DEVNULL)

    return ret


def test_rockyou(new_password):
    with open('/home/zack/Downloads/rockyou.txt', 'r', encoding='ISO-8859-1') as f:
        for attempts, pw in enumerate(f):
            pw = pw.strip()
            found = False
            if pw == new_password:
                ret = str(attempts)
                found = True
                break

        if found == False:
            ret = 'NF'

    return ret


def test_probable_passwords(new_password):
    with open('/home/zack/Downloads/Top304Thousand-probable-v2.txt', 'r', encoding='ISO-8859-1') as f:
        for attempts, pw in enumerate(f):
            pw = pw.strip()
            found = False
            if pw == new_password:
                ret = str(attempts)
                found = True
                break

        if found == False:
            ret = 'NF'

    return ret


def main():
    chdir('/home/zack/Desktop/Hons-Project')
    results = [
        'Old Password,New Password,Custom Wordlist,RockYou Wordlist,Probable Wordlist\n']

    testfile = open('testing/test passwords.txt', 'r').readlines()
    testpasswords = []

    for line in testfile:
        line = line.strip()
        if len(line) > 0:
            if not line.startswith('-'):
                testpasswords.append(tuple(line.split(':')))

    print('Testing on ' + str(len(testpasswords)) + ' passwords')

    for testset in testpasswords:
        results.append(testset[0].replace(',', '') + ',' + testset[1] + ',' + test_custom(testset[0],
                                                                                          testset[1]) + ',' + test_rockyou(testset[1]) + ',' + test_probable_passwords(testset[1]) + '\n')

    print('Testing finished. Saving...')
    outfile = open('testing/testresults.csv', 'w+')
    for result in results:
        outfile.write(result)

    outfile.close()


if __name__ == '__main__':
    main()
