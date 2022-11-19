# findFilterInfo.py - aka extractionRefiner.py - find target elements from html & write them to csv file with same stem as original file
# 22-11-18; 11:00
# source: https://zetcode.com/python/beautifulsoup/

# filters artciles based on text in title or business type
# allowed terms:
# begriffe (in titel (`.NrDZNb`) oder unternehmenstyp - oder generell pauschal in texten von artikel)
# - alternativ*
# - naturheil*
# - heilpraktiker*
# - homoö*

# FEATURE: using pandas dataframes and creation of one search-result-data CSV file (without duplicates), directly from input-HTMLs
#   result: non-duplicates within search results - but still duplicates possible when compared with data_coldCalls.ods! 

from bs4 import BeautifulSoup

import csv
import numpy as np
import os
import pandas as pd
import re


# fileInput = '99996_heilpraktiker'
# fileInput = ['99998_heilpraktiker', '99996_heilpraktiker']
# fileInput = None    # fileInput can be single fileStem-string or list of fileStem-strings - assumption: inputfiles are html's
fileInput = '97725_heilpraktiker'
# fileInput = [
# '97725_heilpraktiker',
# '97727_heilpraktiker',
# '97729_heilpraktiker',
# '97737_heilpraktiker',
# '97753_heilpraktiker',
# '97762_heilpraktiker',
# '97769_heilpraktiker',
# '97772_heilpraktiker',
# '97773_heilpraktiker',
# '97775_heilpraktiker',
# '97776_heilpraktiker',
# '97778_heilpraktiker',
# '97779_heilpraktiker',
# '97780_heilpraktiker',
# '97782_heilpraktiker',
# '97783_heilpraktiker',
# '97785_heilpraktiker',
# '97786_heilpraktiker',
# '97788_heilpraktiker',
# '97789_heilpraktiker',
# '97791_heilpraktiker',
# '97792_heilpraktiker',
# '97794_heilpraktiker',
# '97795_heilpraktiker',
# '97797_heilpraktiker',
# '97799_heilpraktiker',
# '97816_heilpraktiker',
# '97828_heilpraktiker',
# '97833_heilpraktiker',
# '97834_heilpraktiker',
# '97836_heilpraktiker',
# '97837_heilpraktiker',
# '97839_heilpraktiker',
# '97840_heilpraktiker',
# '97842_heilpraktiker',
# '97843_heilpraktiker',
# '97845_heilpraktiker',
# '97846_heilpraktiker',
# '97848_heilpraktiker',
# '97849_heilpraktiker',
# '97851_heilpraktiker',
# '97852_heilpraktiker',
# '97854_heilpraktiker',
# ]

try:
    os.chdir('pwmaps')
except FileNotFoundError as e:
    print('Tried to change to "pwmaps" subdirectory\nDidn\'t find it', e)

def writeInfo2csv(*fileStemList):    # filename only including filename-*stem* (not extension-suffix) - assumption: inputfiles are html's
    resultDfsList = []  # list of dataframes containing all articles of one input-html

    for fileStem in fileStemList:
        print(f'Writing results for: "{fileStem}"...\n')

        resultsList = [] # list of all articles of one input-html (each row represented by a tuple of data for different columns)

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


        # --- get gmaps link, website & guessed job keywords for each article
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

            # --- find job keywords in text of article
            # use IGNORECASE to find results independent of case: https://docs.python.org/3/howto/regex.html#compiling-regular-expressions & https://docs.python.org/3/library/re.html#re.IGNORECASE
            # use bs4's find_all(string=) parameter along with re.compile: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-string-argument
            jobDic = {  # dictionary of potential jobs in article
                'hp': article.find_all(string=re.compile("(heil)|(alternativ)|(homöo)|(osteo)|(akupunk)", re.IGNORECASE)),
                'edu': article.find_all(string=re.compile("(ausbild)|(schule)|(akademie)", re.IGNORECASE)),
                # print(hp)
                'psy': article.find_all(string=re.compile("(psy)", re.IGNORECASE)),
                # print(psy)
                'schwurb': article.find_all(string=re.compile("(energ)|(reiki)", re.IGNORECASE)),
                # print(schwurb)
                'yoga': article.find_all(string=re.compile("(yoga)", re.IGNORECASE)),
                'tier': article.find_all(string=re.compile("(tier)", re.IGNORECASE)),
                'zahn': article.find_all(string=re.compile("(zahn)|(kiefer)", re.IGNORECASE)),
                'physio': article.find_all(string=re.compile("(physio)|(krankengym)", re.IGNORECASE)),
                'ergo': article.find_all(string=re.compile("(ergo)", re.IGNORECASE)),
                'doc': article.find_all(string=re.compile("(arzt)|(ärzt)|(internist)|(allgemeinmedi)|(chirurg)|(ortho)|(radiologe)|(rheumathologe)|(neurologe)", re.IGNORECASE)), # (med) bewusst nicht mit drin, wegen "Alternativmediziner"
                'podo': article.find_all(string=re.compile("(podo)|(fuß)|(fuss)", re.IGNORECASE))
            }
            # print(jobDic)

            # create list of job keys (actual keys of jobDic) which got identified through keywords in text of article
            articleFoundJobsList = [key for key in jobDic if len(jobDic[key]) > 0] # list comprehension to create list of dict-keys if value not empty list: https://stackoverflow.com/a/33077460
            print(articleFoundJobsList)

            articleFoundJobsString = ', '.join(articleFoundJobsList)  # convert list into string: https://www.simplilearn.com/tutorials/python-tutorial/list-to-string-in-python#how_to_convert_a_list_to_string_in_python
            print(articleFoundJobsString)

            # append list of artciles with tuple of found information
            resultsList.append((gMapsHref, websiteLink, articleFoundJobsString))
            print('')
        # print(resultsList)


        # --- create lists of input-HTML-name, Google Business Profile links, websites & found jobs extracted from input-HTML - to create dataframe from lists
        # create list with name of input-HTML file (from which the data got extracted) inserted at the beginning - leading to CSV which has an additional row at the beginning, which shows name of input-HTML in *merged file*- & *link_link*-column - additional row for name of input-HTML to avoid loss of input-HTML-name in case Google Business Profile link in same row is a duplicate (empty *link_link* column would be considered a duplicate - therefore using input-html-name there too)
        mergedFileList = [np.NaN for i in resultsList]  # list (only containing NaN-values) with length of resultsList
        # print(f'mergedFileList: {mergedFileList}')
        mergedFileList.insert(0, f'{fileStem}.html')    # insert item at certain index of list: https://stackoverflow.com/a/17911209
        # print(f'mergedFileList: {mergedFileList}')


        # create lists of Google Business Profile links, websites & found jobs extracted from input-HTML - to create dataframe from lists
        gMapsHrefsList = [f'{fileStem}.html']
        for i,gMapsHref in enumerate(resultsList):
            # print(resultsList[i])        
            gMapsHrefsList.append(resultsList[i][0])
        # print(gMapsHrefsList)

        websiteLinksList = [np.NaN]
        for i,websiteLink in enumerate(resultsList):
            websiteLinksList.append(resultsList[i][1])
        # print(websiteLinksList)

        foundJobsList = [np.NaN]
        for i,articleFoundJobsString in enumerate(resultsList):
            foundJobsList.append(resultsList[i][2])
        # print(foundJobsList)


        # create dataframe from resultsList (which is list of info from all articles in one search)
        resultDf = pd.DataFrame(    # df long as resultsList: create dataframe from list in dictionary: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/#highlighter_83650
            {
                'date': np.NaN,
                'merged file': mergedFileList,
                'link_link': gMapsHrefsList,
                'called (NaN: not available; 1=yes; 0=not interested;)': np.NaN,
                'irrelevant': np.NaN,
                'Erlaubnis nochmal anrufen': np.NaN,
                'hilfsbereit/gesprächig': np.NaN,
                'website': websiteLinksList,
                'Nummer': np.NaN,
                'job': foundJobsList,
                'Notizen': np.NaN
            },
            # index=[0]   # avoid 'ValueError: If using all scalar values, you must pass an index': https://stackoverflow.com/a/17840195
        )

        print(resultDf)

        resultDfsList.append(resultDf)

    # print(resultDfsList)

    newDataDf = pd.concat(resultDfsList).drop_duplicates(['link_link'])   # dataframe of all processed input-HTMLs in one dataframe without duplicates
    print(newDataDf)

    newDataCsvName = f'{fileStemList[0]}-{fileStemList[-1]}.csv'
    newDataDf.to_csv(
        newDataCsvName,
        index=False # turn to True if you want pandas index numbers in first column
        )

    print(f"\nYour output file is called: {newDataCsvName}")









        # # --- write results to csv file for all articles
        # with open(f'{fileStem}.csv', 'w', newline='') as f:  # FEATURE: write statt append weil wir jetzt nur noch ein file ganz am ende schreiben (also keine gefahr mehr resultate aus vorangegangenem loop zu überschreiben)
        #     # UPDATE columns (names or at least order of columns) once you change them in your cold calls file "data_ColdCalls.xlsx"
        #     outputDictWriter = csv.DictWriter(f, ['date', 'merged file', 'link_link', 'called (NaN: not available; 1=yes; 0=not interested;)', 'irrelevant', 'Erlaubnis nochmal anrufen', 'hilfsbereit/gesprächig', 'website', 'Nummer', 'job', 'Notizen'])
        #     outputDictWriter.writeheader()   # FEATURE: write header for every file (so that you can use header names to access columns)

        #     for i,v in enumerate(resultsList):
        #         # print(f'1st: {resultsList[i][0]}')
        #         # print(f'2nd: {resultsList[i][1]}')

        #         # create string of identified jobs from foundJobsList (to write it to csv)
        #         allJobsString = ''
        #         for job in resultsList[i][2]:
        #             allJobsString += f'{job}, '

        #         outputDictWriter.writerow({'link_link': resultsList[i][0], 'website': resultsList[i][1], 'job': allJobsString})


if isinstance(fileInput, str):  # use `isinstance()` to check for type (conditionals): https://stackoverflow.com/a/152596
    writeInfo2csv(fileInput)
elif isinstance(fileInput, list):
    writeInfo2csv(*fileInput)   # use `*args` parameter to accept single & multiple elements as function arguments: https://stackoverflow.com/a/998965
else: # neither string, nor list
    print('Give me a string or list, please!')




# href 0 => google link
# [data-value="Website"] => website
# phone: div mit jsinstance="*1" -> span mit jsinstance="*1" -> egal...





# TODO: make input of script dynamic (create workflow (& programs) to choose set of result-html-files (which match certain naming pattern) & extract their data into csv - instead of just one file every time)
#           maybe make commandline input interactive (argv) - so that you can use it for single files manually AND use it for automation as well?!
#           maybe implement by asking for html file where you want to start & automatically create csv-files from there & for all following files (aka. files with lower plz)