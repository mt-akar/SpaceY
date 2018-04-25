from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

#request = urlopen("https://www.nytimes.com/crosswords/game/mini")
#soup = BeautifulSoup(request.read(), 'html.parser')
#request.close()
soup = BeautifulSoup(open("C:\\SpaceY\\Puzzle htmls\\April 25, 2018 Daily Mini Crossword Puzzle - The New York Times.html"), 'html.parser')
#print(soup.prettify())


''' LAYOUT AND SOLUTION FINDING
g is the array of 25 <g/> which has the text information for the puzzle
layout of the puzzle is found by long inspections, do not question it

note for developer:
print(*soup.find_all('g')[3].find_all('g'), sep="\n")
for i in range(25):
    print(len(soup.find_all('g')[3].find_all('g')[i].find_all('text')))
'''
layList = []
solList = []

g = soup.find_all('g')[3].find_all('g')
lFile = open("layout.txt", "w")
sFile = open("solution.txt", "w")
layoutCounter = 1
for i in range(25):
    allTextsInG = g[i].find_all('text')
    if(len(g[i].find_all('text')) == 0):
        lFile.write("e")
        layList.append('e')
        sFile.write(str(0))
        solList.append('0')

    elif(len(allTextsInG) == 1):
        lFile.write(str(0))
        layList.append('0')
        sFile.write(allTextsInG[0].string)
        solList.append(allTextsInG[0].string)

    elif(len(allTextsInG) == 2):
        lFile.write(str(layoutCounter))
        layList.append(str(layoutCounter))
        layoutCounter+=1
        sFile.write(allTextsInG[1].string)
        solList.append(allTextsInG[1].string)
    else:
        print("Unexpected assumption error.")
lFile.close()
sFile.close()


'''START POSITION AND LEGNTH FINDING
'''
lenList = []

for i in range(5):
    leng = 0
    for j in range(5):
        if(layList[i*5 + j] != 'e'):
            leng = leng + 1
    lenList.append(leng)
for i in range(5):
    leng = 0
    for j in range(5):
        if(layList[i + j*5] != 'e'):
            leng = leng + 1
    lenList.append(leng)

startList = []

for i in range(5):
    j=0
    start = i*5 + j
    while(layList[start] == 'e'):
        j += 1
        start = i*5 + j
    startList.append(i*5 + j)
for i in range(5):
    j=0
    start = i + j*5
    while(layList[start] == 'e'):
        j += 1
        start = i + j*5
    startList.append(i + j*5)


''' CLUE FINDING
List is the list of clues
text of clues are found by long inspections, do not question it

note for developer:
print(*soup.find_all('span'), sep="\n")
'''
cList = ['', '', '', '', '', '', '', '', '', '']
cFile = open("clues.txt", "w")
for i in range(10):
    if(i<5):
        cList[i] = soup.find_all('span')[2*i+5].string
    else:
        for j in range(15):
            if(layList[j] == str(i - 4)):
                break
        cList[startList[i] % 5 + 5] = soup.find_all('span')[2*i+5].string
    cFile.write(soup.find_all('span')[2*i+4].string + ") " + cList[i] + "\n")
cFile.close()


''' TITLE FINDING
'''
tFile = open("title.txt", "w")
tFile.write(soup.find_all("title")[0].string)
tFile.close()


''' POSSIBLE ANSWERS
'''
answers = [[], [], [], [], [], [], [], [], [], []]

def addToPossibleList(k, length, text):
    text = text.upper()
    for i in range(len(text) - length - 1):
        b = True
        if(text[i].isalpha()):
            b = False
        for j in range(length):
            if(text[i + j + 1].isalpha() == False):
                b = False
        if(text[i + length + 1].isalpha()):
            b = False
        if(b and text[i + 1 : i + length + 1] not in answers[k]):
            
            for j in range(length):
                if(k<5 and text[i + 1 + j] == solList[startList[k] + j] or 
                    k>=5 and text[i + 1 + j] == solList[startList[k] + j*5]):

                    print(k, text[i + 1 : i + length + 1], end=' ')
                    answers[k].append(text[i + 1 : i + length + 1])
                    break

''' THESARUS
'''
print("Thesarus begins")

for k in range(10):
    print('\n' + str(k))
    try:
        while(True):
            url = 'http://www.thesaurus.com/browse/' + cList[k].replace(' ', '%20') + '?s=ts'
            print(url)
            page = urlopen(url)
            thesarusSoup = BeautifulSoup(page, 'html.parser')
            if(len(thesarusSoup.find_all('script')) > 15):
                print(str(len(thesarusSoup.find_all('script'))) + ' error')
            else:
                break
    except:
        print('thesarus exception')
        continue
    
    print(len(thesarusSoup.find_all('script')))
    if(len(thesarusSoup.find_all('script')) == 11):
        continue

    addToPossibleList(k, lenList[k], thesarusSoup.find_all('script')[10].string)
    addToPossibleList(k, lenList[k], thesarusSoup.find_all('script')[10].string.replace(' ', ''))


''' WIKIPADIA
'''
print("Wikipedia begins")

for k in range(10):
    print('\n' + str(k))
    text = ''
    try:
        url = 'https://en.wikipedia.org/w/index.php?search=' + cList[k].replace(' ', '+')
        page = urlopen(url)
        wikiSoup = BeautifulSoup(page, 'html.parser')
        text = str(wikiSoup)
    except:
        print('error occured in first phase of wiki search')
        continue
    try:
        url = 'https://en.wikipedia.org' + wikiSoup.find_all('ul')[1].find_all('a')[0]['href']
        page = urlopen(url)
        wikiSoup = BeautifulSoup(page, 'html.parser')
        text = str(wikiSoup)
        print('try worked')
        print(url)
        if(url != 'https://en.wikipedia.org/wiki/Special:MyTalk'):
            addToPossibleList(k, lenList[k], text)
    except:
        print('try didn\'t work')
        addToPossibleList(k, lenList[k], text)















'''
import webbrowser
query = 'genetic material'
url = "https://www.google.co.in/search?q=" + (str(query)) + "&oq=" + (
str(query)) + "&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
webbrowser.open(url)
'''