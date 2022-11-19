# findInfo2.py - find target elements from html & write them to csv file with same stem as original file
# 22-11-14; 11:15

# source: https://zetcode.com/python/beautifulsoup/

# NEW FEATURES:
#   accept either list or string as input for writeInfo2csv() - using script to call function correctly depending on input type
#   ability to convert lists of files by writing them as list at beginning of file (assigned to variable "fileInput")


from bs4 import BeautifulSoup

import csv
import os


# fileInput = 'plumber_new york city'  # without file extension
# fileInput = 'carpenter_london'
# fileInput = '99998_heilpraktiker'
# fileInput = '99996_heilpraktiker'
# fileInput = ['99998_heilpraktiker', '99996_heilpraktiker']
# fileInput = None    # fileInput can be single fileStem-string or list of fileStem-strings - assumption: inputfiles are html's
fileInput = [
'99976_heilpraktiker',
'99958_heilpraktiker',
'99974_heilpraktiker',
]

try:
    os.chdir('pwmaps')
except FileNotFoundError:
    pass

def writeInfo2csv(*fileStemList):    # filename only including filename-*stem* (not extension-suffix) - assumption: inputfiles are html's
    for fileStem in fileStemList:
        print(f'Writing results for: "{fileStem}"...\n')

        resultsList = []

        with open(f'{fileStem}.html', 'r') as f:

            contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            # print(soup.select('li:nth-of-type(3)'))
            allArticles = soup.select('[role="article"]')  # watch out: limited CSS selectors in bs4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors -> https://facelessuser.github.io/soupsieve/
            # print(type(allArticles))
            # print(len(allArticles))

            # # --- get gmaps link & website for 1st article
            # article = allArticles[0]
            # # print(article)
            # gMapsHref = article.select_one('a').get('href')
            # # print(gMapsHref)

            # websiteLink = article.select_one('[data-value="Website"]').get('href')
            # # print(websiteLink)

            # # firstArticle = soup.select_one('[role="article"]')  # watch out: limited CSS selectors in bs4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors -> https://facelessuser.github.io/soupsieve/
            # # with open(f'{fileStem}_1.html', 'w') as f:
            # #     f.write(str(firstArticle))

            # # --- write results to csv file for 1st artcile
            # # with open(f'{fileStem}_1.csv', 'w', newline='') as f:
            # #     outputDictWriter = csv.DictWriter(f, ['date', 'merged file', 'link_link', 'called (NaN: not available; 1=yes; 0=not interested;)', 'irrelevant', 'Erlaubnis nochmal anrufen', 'hilfsbereit/gesprächig', 'website', 'Nummer', 'Notizen'])
            # #     outputDictWriter.writeheader()
            # #     outputDictWriter.writerow({'link_link': gMapsHref, 'website': websiteLink})

        # print(type(allArticles))
        # print(len(allArticles))


        # --- get gmaps link & website for all articles
        for article in allArticles:
            gMapsHref = article.select_one('a').get('href')
            print(gMapsHref)

            try:
                websiteLink = article.select_one('[data-value="Website"]').get('href')
                # print('type of website link: ', type(websiteLink))
                if websiteLink != None:
                    print(websiteLink)
                elif websiteLink == None:
                    print('no website link')
            except AttributeError as e:
                print('error: ', e)
                if "'NoneType' object has no attribute 'get'" in str(e):
                    websiteLink = 0
                    print('no website link')

            resultsList.append((gMapsHref, websiteLink))    
            print('')


        # --- write results to csv file for all articles
        with open(f'{fileStem}.csv', 'w', newline='') as f:  # FEATURE: write statt append weil wir jetzt nur noch ein file ganz am ende schreiben (also keine gefahr mehr resultate aus vorangegangenem loop zu überschreiben)
            # UPDATE columns (names or at least order of columns) once you change them in your cold calls file "data_ColdCalls.xlsx"
            outputDictWriter = csv.DictWriter(f, ['date', 'merged file', 'link_link', 'called (NaN: not available; 1=yes; 0=not interested;)', 'irrelevant', 'Erlaubnis nochmal anrufen', 'hilfsbereit/gesprächig', 'website', 'Nummer', 'Notizen'])
            outputDictWriter.writeheader()   # FEATURE: write header for every file (so that you can use header names to access columns)

            for i,v in enumerate(resultsList):
                # print(f'1st: {resultsList[i][0]}')
                # print(f'2nd: {resultsList[i][1]}')
                outputDictWriter.writerow({'link_link': resultsList[i][0], 'website': resultsList[i][1]})


if isinstance(fileInput, str):
    writeInfo2csv(fileInput)
elif isinstance(fileInput, list):
    writeInfo2csv(*fileInput)
else: # neither string, nor list
    print('Give me a string or list, please!')




# href 0 => google link
# [data-value="Website"] => website
# phone: div mit jsinstance="*1" -> span mit jsinstance="*1" -> egal...





# TODO: make input of script dynamic (create workflow (& programs) to choose set of result-html-files (which match certain naming pattern) & extract their data into csv - instead of just one file every time)
#           maybe make commandline input interactive (argv) - so that you can use it for single files manually AND use it for automation as well?!
#           maybe implement by asking for html file where you want to start & automatically create csv-files from there & for all following files (aka. files with lower plz)