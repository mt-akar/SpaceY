from urllib.request import urlopen
from bs4 import BeautifulSoup

#request = urlopen("https://www.nytimes.com/crosswords/game/mini")
#soup = BeautifulSoup(request.read(), 'html.parser')
#request.close()
soup = BeautifulSoup(open("C:\\SpaceY\\Puzzle htmls\\March 9, 2018 Daily Mini Crossword Puzzle - The New York Times.html"), 'html.parser')
#print(soup.prettify())
w=8

''' CLEAR UI OUTPUTS
'''
eventFile = open("eventLog.txt", "w")
eventFile.close()

guessFile = open("guess.txt", "w")
for i in range(25):
    guessFile.write('-')
guessFile.close()

''' LAYOUT AND SOLUTION FINDING
g is the array of 25 <g/> which has the text information for the puzzle
layout of the puzzle is found by long inspections, do not question it

note for developer:
print(*soup.find_all('g')[3].find_all('g'), sep="\n")
for i in range(25):
    print(len(soup.find_all('g')[3].find_all('g')[i].find_all('text')))
'''
eventFile = open("eventLog.txt", "a")
eventFile.write('Pulling puzzle layout and solutions...\n')
eventFile.close()

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


''' START POSITION AND LEGNTH FINDING
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
eventFile = open("eventLog.txt", "a")
eventFile.write('Pulling clues...\n')
eventFile.close()

cList = ['', '', '', '', '', '', '', '', '', '']
cFile = open("clues.txt", "w")
for i in range(10):
    if(i<5):
        cList[i] = soup.find_all('span')[2*i+w].string
    else:
        for j in range(15):
            if(layList[j] == str(i - 4)):
                break
        cList[startList[i] % 5 + 5] = soup.find_all('span')[2*i+w].string
    cFile.write(soup.find_all('span')[2*i+w-1].string + ") " + cList[i] + "\n")
cFile.close()

clueList = ['', '', '', '', '', '', '', '', '', '']
for i in range(5):
    clueList[i] = cList[i].replace('"', '').replace('_', '')
c = 5
for i in range(15):
    if(layList[i] != 'e' and clueList[i%5 + 5] == ''):
        clueList[i%5 + 5] = cList[c].replace('"', '').replace('_', '')
        c += 1

''' TITLE FINDING
'''
tFile = open("title.txt", "w")
tFile.write(soup.find_all("title")[0].string)
tFile.close()


''' POSSIBLE ANSWERS
'''
answers = [[], [], [], [], [], [], [], [], [], []]
add = 'HO'

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
                if(k<5 and text[i + 1 + j] == solList[startList[k] + j] and abs(ord(text[i + 3]) - ord(solList[startList[k] + 2])) < 5 and
                    abs(ord(text[i + 2]) - ord(solList[startList[k] + 1])) < 5 or 
                    k>=5 and text[i + 1 + j] == solList[startList[k] + j*5] and abs(ord(text[i + 3]) - ord(solList[startList[k] + 10])) < 5 and
                    abs(ord(text[i + 2]) - ord(solList[startList[k] + 5])) < 5):
                    
                    eventFile = open("eventLog.txt", "a")
                    eventFile.write(' ' + text[i + 1 : i + length + 1])
                    eventFile.close()
                    print(text[i + 1 : i + length + 1], end=' ')
                    answers[k].append(text[i + 1 : i + length + 1])
                    break

def addToPossibleListThesarus(k, length, text):
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
                if(k<5 and text[i + 1 + j] == solList[startList[k] + j] and abs(ord(text[i + 3]) - ord(solList[startList[k] + 2])) < 5 or 
                    k>=5 and text[i + 1 + j] == solList[startList[k] + j*5] and abs(ord(text[i + 3]) - ord(solList[startList[k] + 10])) < 5):
                    
                    eventFile = open("eventLog.txt", "a")
                    eventFile.write(' ' + text[i + 1 : i + length + 1])
                    eventFile.close()
                    print(text[i + 1 : i + length + 1], end=' ')
                    answers[k].append(text[i + 1 : i + length + 1])
                    break


''' WIKIPADIA
'''
eventFile = open("eventLog.txt", "a")
eventFile.write('\nSearching WIKIPEDIA.COM for possible answers...\n')
eventFile.close()
print("Wikipedia begins")

for k in range(10):
    print('\n\n' + str(k))
    eventFile = open("eventLog.txt", "a")
    eventFile.write('Searching wikipedia.com for \"' + clueList[k] + '\"...\n')
    eventFile.close()
    text = ''
    try:
        url = 'https://en.wikipedia.org/w/index.php?search=' + clueList[k].replace(' ', '+')
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
        
            eventFile = open("eventLog.txt", "a")
            eventFile.write('Possible answers:')
            eventFile.close()

            addToPossibleList(k, lenList[k], text)

            eventFile = open("eventLog.txt", "a")
            eventFile.write('\n\n')
            eventFile.close()
    except:
        print('try didn\'t work')

        eventFile = open("eventLog.txt", "a")
        eventFile.write('Possible answers:')
        eventFile.close()

        addToPossibleList(k, lenList[k], text)
        
        eventFile = open("eventLog.txt", "a")
        eventFile.write('\n')
        eventFile.close()


''' THESARUS
'''
eventFile = open("eventLog.txt", "a")
eventFile.write('\nSearching THESARUS.COM for possible answers...\n')
eventFile.close()
print("Thesarus begins")

for k in range(10):
    print('\n' + str(k))
    eventFile = open("eventLog.txt", "a")
    eventFile.write('Searching thesarus.com for \"' + clueList[k] + '\"...\n')
    eventFile.close()
    try:
        while(True):
            url = 'http://www.thesaurus.com/browse/' + clueList[k].replace(' ', '%20') + '?s=ts'
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

    if(isinstance(thesarusSoup.find_all('script')[10].string,str)):
        
        eventFile = open("eventLog.txt", "a")
        eventFile.write('Possible answers:')
        eventFile.close()

        addToPossibleListThesarus(k, lenList[k], thesarusSoup.find_all('script')[10].string)
        addToPossibleListThesarus(k, lenList[k], thesarusSoup.find_all('script')[10].string.replace(' ', ''))

        eventFile = open("eventLog.txt", "a")
        eventFile.write('\n\n')
        eventFile.close()


''' MERRIAM
'''
eventFile = open("eventLog.txt", "a")
eventFile.write('\nSearching MERRIAM-WEBSTER.COM for possible answers...\n')
eventFile.close()
print("Merriam begins")

for k in range(10):
    print('\n' + str(k))
    eventFile = open("eventLog.txt", "a")
    eventFile.write('Searching merriam-webster.com for \"' + clueList[k] + '\"...\n')
    eventFile.close()
    try:
        url = 'https://www.merriam-webster.com/dictionary/' + clueList[k].replace(' ', '%20')
        print(url)
        page = urlopen(url)
        meriamSoup = BeautifulSoup(page, 'html.parser')
    except:
        print('meriam exception')
        continue

    eventFile = open("eventLog.txt", "a")
    eventFile.write('Possible answers:')
    eventFile.close()

    addToPossibleList(k, lenList[k], str(meriamSoup.find_all('p')[9]))

    eventFile = open("eventLog.txt", "a")
    eventFile.write('\n\n')
    eventFile.close()
rem = 'RN'


''' ADD JOKER WORDS FOR CLUES THAT ARE LEFT BLANK
'''
for i in range(10):
    joker = ''
    for j in range(lenList[i]):
        joker += '0'
    answers[i].append(joker)
answers[5].append(add + rem)


''' GUESS THE FINAL SOLUTION FROM FOUND POSSIBLE ANSWERS
'''
import numpy as np

maxPoint = 0
for i0 in answers[0]:
    print(i0)
    for i5 in answers[5]:

        if(layList[0] != 'e' and i0[0] != '0' and i5[0] != '0' and i0[0] != i5[0]):
            continue
        
        for i1 in answers[1]:
            
            columnC = i5[(5 - startList[5]) // 5]

            if(layList[5] != 'e' and i1[0] != '0' and columnC != '0' and i1[0] != columnC):
                continue
            
            for i6 in answers[6]:

                break6 = False
                for j6 in np.linspace(1, 6, 2, dtype = int):

                    if(layList[j6] == 'e'):
                        continue

                    rowN = j6//5
                    if(rowN == 0):
                        row = i0
                    elif(rowN == 1):
                        row = i1
                    
                    column = i6

                    rowC = row[j6 - startList[rowN]]
                    columnC = column[(j6 - startList[6]) // 5]

                    if(rowC != '0' and columnC != '0' and rowC != columnC):
                        break6 = True
                        break

                if(break6):
                    continue
                
                for i2 in answers[2]:

                    break2 = False
                    for j2 in np.linspace(10, 11, 2, dtype = int):

                        if(layList[j2] == 'e'):
                            continue

                        row = i2
                        
                        columnN = j2%5 + 5
                        if(columnN == 5):
                            column = i5
                        elif(columnN == 6):
                            column = i6

                        rowC = row[j2 - startList[2]]
                        columnC = column[(j2 - startList[columnN]) // 5]

                        if(rowC != '0' and columnC != '0' and rowC != columnC):
                            break2 = True
                            break

                    if(break2):
                        continue

                    for i7 in answers[7]:

                        break7 = False
                        for j7 in np.linspace(2, 12, 3, dtype = int):

                            if(layList[j7] == 'e'):
                                continue

                            rowN = j7//5
                            if(rowN == 0):
                                row = i0
                            elif(rowN == 1):
                                row = i1
                            elif(rowN == 2):
                                row = i2
                            
                            column = i7

                            rowC = row[j7 - startList[rowN]]
                            columnC = column[(j7 - startList[7]) // 5]

                            if(rowC != '0' and columnC != '0' and rowC != columnC):
                                break7 = True
                                break

                        if(break7):
                            continue
                
                        for i3 in answers[3]:

                            break3 = False
                            for j3 in np.linspace(15, 17, 3, dtype = int):

                                if(layList[j3] == 'e'):
                                    continue

                                row = i3
                                
                                columnN = j3%5 + 5
                                if(columnN == 5):
                                    column = i5
                                elif(columnN == 6):
                                    column = i6
                                elif(columnN == 7):
                                    column = i7

                                rowC = row[j3 - startList[3]]
                                columnC = column[(j3 - startList[columnN]) // 5]

                                if(rowC != '0' and columnC != '0' and rowC != columnC):
                                    break3 = True
                                    break

                            if(break3):
                                continue

                            for i8 in answers[8]:

                                break8 = False
                                for j8 in np.linspace(3, 18, 4, dtype = int):

                                    if(layList[j8] == 'e'):
                                        continue

                                    rowN = j8//5
                                    if(rowN == 0):
                                        row = i0
                                    elif(rowN == 1):
                                        row = i1
                                    elif(rowN == 2):
                                        row = i2
                                    elif(rowN == 3):
                                        row = i3
                                    
                                    column = i8

                                    rowC = row[j8 - startList[rowN]]
                                    columnC = column[(j8 - startList[8]) // 5]

                                    if(rowC != '0' and columnC != '0' and rowC != columnC):
                                        break8 = True
                                        break

                                if(break8):
                                    continue
                
                                for i4 in answers[4]:

                                    break4 = False
                                    for j4 in np.linspace(20, 23, 4, dtype = int):

                                        if(layList[j4] == 'e'):
                                            continue

                                        row = i4
                                        
                                        columnN = j4%5 + 5
                                        if(columnN == 5):
                                            column = i5
                                        elif(columnN == 6):
                                            column = i6
                                        elif(columnN == 7):
                                            column = i7
                                        elif(columnN == 8):
                                            column = i8

                                        rowC = row[j4 - startList[4]]
                                        columnC = column[(j4 - startList[columnN]) // 5]

                                        if(rowC != '0' and columnC != '0' and rowC != columnC):
                                            break4 = True
                                            break

                                    if(break4):
                                        continue

                                    for i9 in answers[9]:

                                        break9 = False
                                        for j9 in np.linspace(4, 24, 5, dtype = int):

                                            if(layList[j9] == 'e'):
                                                continue

                                            rowN = j9//5
                                            if(rowN == 0):
                                                row = i0
                                            elif(rowN == 1):
                                                row = i1
                                            elif(rowN == 2):
                                                row = i2
                                            elif(rowN == 3):
                                                row = i3
                                            elif(rowN == 4):
                                                row = i4
                                            
                                            column = i9

                                            rowC = row[j9 - startList[rowN]]
                                            columnC = column[(j9 - startList[9]) // 5]

                                            if(rowC != '0' and columnC != '0' and rowC != columnC):
                                                break9 = True
                                                break

                                        if(break9):
                                            continue
                                        
                                        rowPoint = 1
                                        if(i0[0] != '0'):
                                            rowPoint += 1
                                        if(i1[0] != '0'):
                                            rowPoint += 1
                                        if(i2[0] != '0'):
                                            rowPoint += 1
                                        if(i3[0] != '0'):
                                            rowPoint += 1
                                        if(i4[0] != '0'):
                                            rowPoint += 1
                                        
                                        columnPoint = 1
                                        if(i5[0] != '0'):
                                            columnPoint += 1
                                        if(i6[0] != '0'):
                                            columnPoint += 1
                                        if(i7[0] != '0'):
                                            columnPoint += 1
                                        if(i8[0] != '0'):
                                            columnPoint += 1
                                        if(i9[0] != '0'):
                                            columnPoint += 1
                                        
                                        if(rowPoint * columnPoint > maxPoint):
                                            
                                            eventFile = open("eventLog.txt", "a")
                                            eventFile.write('New possible solution: ' + i0 + ' ' + i1 + ' ' + i2 + ' ' + i3 + ' ' + i4 + ' ' + i5 + ' ' + i6 + ' ' + i7 + ' ' + i8 + ' ' + i9)
                                            eventFile.write('\nSolution confidence: ' + str(rowPoint * columnPoint) + '/36\n\n')
                                            eventFile.close()

                                            print(rowPoint * columnPoint,i0,i1,i2,i3,i4,i5,i6,i7,i8,i9)

                                        if(rowPoint * columnPoint > maxPoint):
                                            maxPoint = rowPoint * columnPoint
                                            guess = [i0, i1, i2, i3, i4, i5, i6, i7, i8, i9]
                                            guessTable = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                                            for u in range(10):
                                                for y in range(lenList[u]):
                                                    if(u<5 and (guess[u])[y] != '0'):
                                                        guessTable[startList[u] + y] = (guess[u])[y]
                                                    elif((guess[u])[y] != '0'):
                                                        guessTable[startList[u] + y*5] = (guess[u])[y]

                                            guessFile = open("guess.txt", "w")
                                            for p in range(25):
                                                if(guessTable[p] == '' or guessTable[p] == '0'):
                                                    guessFile.write('-')
                                                else:
                                                    guessFile.write(guessTable[p])
                                            guessFile.close()

'''
for i0 in answers[0]:
    for i1 in answers[1]:
        print(i1)
        for i2 in answers[2]:
            for i3 in answers[3]:
                for i4 in answers[4]:
                    for i5 in answers[5]:

                        break5 = False
                        for j5 in np.linspace(0, 20, 5, dtype = int):

                            if(layList[j5] == 'e'):
                                continue

                            rowN = j5//5
                            if(rowN == 0):
                                row = i0
                            elif(rowN == 1):
                                row = i1
                            elif(rowN == 2):
                                row = i2
                            elif(rowN == 3):
                                row = i3
                            elif(rowN == 4):
                                row = i4
                            
                            column = i5

                            rowC = row[0]
                            columnC = column[(j5 - startList[5]) // 5]

                            if(rowC != '0' and columnC != '0' and rowC != columnC):
                                break5 = True
                                break

                        if(break5):
                            break

                        for i6 in answers[6]:

                            break6 = False
                            for j6 in np.linspace(1, 21, 5, dtype = int):

                                if(layList[j6] == 'e'):
                                    continue

                                rowN = j6//5
                                if(rowN == 0):
                                    row = i0
                                elif(rowN == 1):
                                    row = i1
                                elif(rowN == 2):
                                    row = i2
                                elif(rowN == 3):
                                    row = i3
                                elif(rowN == 4):
                                    row = i4
                                
                                column = i6

                                rowC = row[j6 - startList[rowN]]
                                columnC = column[(j6 - startList[6]) // 5]

                                if(rowC != '0' and columnC != '0' and rowC != columnC):
                                    break6 = True
                                    break

                            if(break6):
                                break

                            for i7 in answers[7]:

                                break7 = False
                                for j7 in np.linspace(2, 22, 5, dtype = int):

                                    if(layList[j7] == 'e'):
                                        continue

                                    rowN = j7//5
                                    if(rowN == 0):
                                        row = i0
                                    elif(rowN == 1):
                                        row = i1
                                    elif(rowN == 2):
                                        row = i2
                                    elif(rowN == 3):
                                        row = i3
                                    elif(rowN == 4):
                                        row = i4
                                    
                                    column = i7

                                    rowC = row[j7 - startList[rowN]]
                                    columnC = column[(j7 - startList[7]) // 5]

                                    if(rowC != '0' and columnC != '0' and rowC != columnC):
                                        break7 = True
                                        break

                                if(break7):
                                    break

                                for i8 in answers[8]:

                                    break8 = False
                                    for j8 in np.linspace(3, 23, 5, dtype = int):

                                        if(layList[j8] == 'e'):
                                            continue

                                        rowN = j8//5
                                        if(rowN == 0):
                                            row = i0
                                        elif(rowN == 1):
                                            row = i1
                                        elif(rowN == 2):
                                            row = i2
                                        elif(rowN == 3):
                                            row = i3
                                        elif(rowN == 4):
                                            row = i4
                                        
                                        column = i8

                                        rowC = row[j8 - startList[rowN]]
                                        columnC = column[(j8 - startList[8]) // 5]

                                        if(rowC != '0' and columnC != '0' and rowC != columnC):
                                            break8 = True
                                            break

                                    if(break8):
                                        break

                                    for i9 in answers[9]:

                                        break9 = False
                                        for j9 in np.linspace(4, 24, 5, dtype = int):

                                            if(layList[j9] == 'e'):
                                                continue

                                            rowN = j9//5
                                            if(rowN == 0):
                                                row = i0
                                            elif(rowN == 1):
                                                row = i1
                                            elif(rowN == 2):
                                                row = i2
                                            elif(rowN == 3):
                                                row = i3
                                            elif(rowN == 4):
                                                row = i4
                                            
                                            column = i9

                                            rowC = row[j9 - startList[rowN]]
                                            columnC = column[(j9 - startList[9]) // 5]

                                            if(rowC != '0' and columnC != '0' and rowC != columnC):
                                                break9 = True
                                                break

                                        if(break9):
                                            break
'''




'''
for i0 in answers[0]:
    for i1 in answers[1]:
        print(i1)
        for i2 in answers[2]:
            for i3 in answers[3]:
                for i4 in answers[4]:
                    for i5 in answers[5]:
                        for i6 in answers[6]:
                            for i7 in answers[7]:
                                for i8 in answers[8]:
                                    for i9 in answers[9]:
                                        for j in range(25):

                                            if(layList[j] == 'e'):
                                                continue

                                            rowN = j//5
                                            if(rowN == 0):
                                                row = i0
                                            elif(rowN == 1):
                                                row = i1
                                            elif(rowN == 2):
                                                row = i2
                                            elif(rowN == 3):
                                                row = i3
                                            elif(rowN == 4):
                                                row = i4
                                            
                                            columnN = j%5 + 5
                                            if(columnN == 5):
                                                column = i5
                                            elif(columnN == 6):
                                                column = i6
                                            elif(columnN == 7):
                                                column = i7
                                            elif(columnN == 8):
                                                column = i8
                                            elif(columnN == 9):
                                                column = i9
                                            
                                            rowC = row[j - startList[rowN]]
                                            columnC = column[(j - startList[columnN]) // 5]

                                            #print(j, rowC, columnC)
                                            if(rowC != '0' and columnC != '0' and rowC != columnC):
                                                break

                                        if(columnN < 9):
                                            break
                                    if(columnN < 8):
                                        break
                                if(columnN < 7):
                                        break
                            if(columnN < 6):
                                    break
                    if(rowN < 4):
                        break
                if(rowN < 3):
                    break
            if(rowN < 2):
                break
        if(rowN <1):
            break
'''                       













'''
url = 'https://www.google.com.tr/search?ei=B83gWq6xJ4_8kwWr25O4Ag&q=hello&oq=hello&gs_l=psy-ab.3..35i39k1j0i67k1l9.7377.8659.0.8848.6.6.0.0.0.0.144.498.0j4.5.0....0...1c.1.64.psy-ab..1.5.631.6..0j0i20i263k1.137.K_SBqYzi7vg'
page = urlopen(url)
wikiSoup = BeautifulSoup(page, 'html.parser')
text = str(wikiSoup)
print(text)


import webbrowser
query = 'genetic material'
url = "https://www.google.co.in/search?q=" + (str(query)) + "&oq=" + (
str(query)) + "&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
webbrowser.open(url)
'''
