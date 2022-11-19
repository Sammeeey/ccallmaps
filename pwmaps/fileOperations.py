# fileOperations.py - functions to find and/or modify files which match certain patterns

from pathlib import Path

import os
import sys


def findByCriterion(criterion, dirPath=Path.cwd()):
    """
    - dirPath: takes pathlib.Path path for directory
    - criterion: takes glob pattern (unix filename pattern): https://docs.python.org/3/library/fnmatch.html#module-fnmatch
    - finds files in specified directory (dirPath) based on certain glob pattern (criterion) & saves them in a list

    returns (possibly empty) list of pathlib.Path file-paths, which match specified criterion inside specified directory
    """

    # identify all files in target directory, which match certain criterion (originally all those which match glob pattern)
    p = dirPath
    print(f'Finding first file in...\n{p}\n...which matches this criterion:{criterion}\n')
    # filePathList = list(p.glob(criterion))
    filePathList = sorted(p.glob(criterion))    # build ascending list: https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob & https://docs.python.org/3/howto/sorting.html#sorting-basics

    return filePathList


def switchName(criterion, pathList):
    """
    originated from: switchName.py - script finds 'heilpraktiker_*.html' files in current working directory and renames it by switching order of words between '_'
            - switches e.g. from 'heilpraktiker_99518.html' to '99518_heilpraktiker.html'

    WARNING!!!!!!!WARNING!!!!!!
    will also switch names of error files BUT(!) in the wrong way!
    WARNING!!!!!!!WARNING!!!!!!
    """
    if len(pathList) > 0:
        print(f'Will use file:\n{pathList}\n')
        # print(type(pathList))

        for file in pathList:
            # print(file.name)
            print(file.stem)    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.stem
            stemPartsList = file.stem.split('_')
            switchList = stemPartsList[::-1]    # https://stackoverflow.com/a/509295
            print(switchList)
            newStem = '_'.join(switchList)
            newName = newStem + file.suffix
            print(f'new filename: {newName}')

            # rename file
            os.rename(file.name, newName)   # https://stackoverflow.com/a/2491232

    else: # if len(pathList) <= 0:
        print(f'Looks like there is no file, which matches the glob pattern: {criterion}')
        print('Please make sure there is one.\nThen run the script again...')
        sys.exit()


def find1stfilePart(criterion, dirPath=Path.cwd()):
    """
    - finds all files specified directory, based on certain pattern (see findbyCriterion()) & saves them in a list

    returns:
    - string: first part of stem (before '_') of first file (from list of files which matched criterion)
    - None: if no file matches criterion (aka. list of found files empty)
    """
    fileList = findByCriterion(criterion, dirPath)
    # print('List of files which match the criterion:', fileList)

    if len(fileList) > 0:
        firstFile = fileList[0]
        print('Found file here:\n', firstFile)

        # print(firstFile.stem)    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.stem
        stemPartsList = firstFile.stem.split('_')
        firstFilePart = stemPartsList[0]
        
        return firstFilePart

    else: # if len(pathList) <= 0:
        print(f'Looks like there is no file, which matches the glob pattern: {criterion}')
        # print('Please make sure there is one.\nThen run the script again...')


# # --- find by criterion
# targetGroup = 'heilpraktiker'
# resultList = findByCriterion(fr'*_{targetGroup}.html')
# print(resultList)



# # --- switch name: finds 'heilpraktiker_*.html' files in current working directory and renames it by switching order of words between '_'
# #      - switches e.g. from 'heilpraktiker_99518.html' to '99518_heilpraktiker.html'
# fpathList = findByCriterion('heilpraktiker_*.html', Path.cwd())
# switchName('heilpraktiker_*.html', fpathList)




# # --- find plz of latest successful html file from search
# # RegEx pattern: \d+_(heilpraktiker).html -> matches 99518_heilpraktiker.html ; but doesn't match 99518_heilpraktiker_error.html
# #   but unix filename pattern (fr'*_heilpraktiker.html') needed instead of RegEx: https://stackoverflow.com/a/36295481

# # assumption: main program runs though list of descending zip codes & saves results as [PLZ]_heilpraktiker.html or if it fails as [PLZ]_heilpraktiker_error.html
# targetGroup = 'heilpraktiker'

# latestSuccessPlz = find1stfilePart(fr'*_{targetGroup}.html')
# print('1st file part:', latestSuccessPlz)