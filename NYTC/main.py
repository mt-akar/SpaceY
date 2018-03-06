from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

#request = urlopen("https://www.nytimes.com/crosswords/game/mini")
#soup = BeautifulSoup(request.read(), 'html.parser')
#request.close()
soup = BeautifulSoup(open("C:\\SpaceY\\Puzzle page info\\05.03\\March 5, 2018 Daily Mini Crossword Puzzle - The New York Times.html"), 'html.parser')
# print(soup.prettify())


''' LAYOUT AND SOLUTION FINDING
g is the array of 25 <g/> which has the text information for the puzzle
layout of the puzzle is found by long inspections, do not question it

note for developer:
print(*soup.find_all('g')[3].find_all('g'), sep="\n")
for i in range(25):
    print(len(soup.find_all('g')[3].find_all('g')[i].find_all('text')))
'''
g = soup.find_all('g')[3].find_all('g')

lFile = open("layout.txt", "w")
sFile = open("solution.txt", "w")
layoutCounter = 1
for i in range(25):
    allTextsInG = g[i].find_all('text')
    if(len(g[i].find_all('text')) == 0):
        lFile.write("e")
        sFile.write(str(0))
    elif(len(allTextsInG) == 1):
        lFile.write(str(0))
        sFile.write(allTextsInG[0].string)
    elif(len(allTextsInG) == 2):
        lFile.write(str(layoutCounter))
        sFile.write(allTextsInG[1].string)
        layoutCounter+=1
    else:
        print("Unexpected assumption error.")
lFile.close()
sFile.close()

''' CLUE FINDING
qList is the list of clues
text of clues are find by long inspections, do not question it

note for developer:
print(*soup.find_all('span'), sep="\n")
'''
cList = []
cFile = open("clues.txt", "w")
for i in range(10):
    cList.append(soup.find_all('span')[2*i+8].string)
    cFile.write(soup.find_all('span')[2*i+7].string + ") " + cList[i] + "\n")
cFile.close()

''' TITLE FINDING
'''
tFile = open("title.txt", "w")
tFile.write(soup.find_all("title")[0].string)

print("append section")

for i in range(1):
    outFile = open("eventLog.txt", "a")
    outFile.write("I am doing something\n")
    outFile.close()