import random
import string
import time

for j in range(1):
    outFile = open("guess.txt", "w")
    for i in range(25):
        outFile.write(random.choice(string.ascii_uppercase))
    outFile.close()
    time.sleep(1)



    '''
allSpan = soup.find_all('span')

qFile = open("questions.txt", "w")
for i in range(10):
    qFile.write(allSpan[2*i+5].string + "\n")
'''