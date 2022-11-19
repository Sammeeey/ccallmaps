# callmaps aka. pwmaps
> built & tested using Python 3.9.7

- framework aka. programs and workflows to collect data from Google Maps (as HTML) & extract it to a format (CSV) in which it can be used to do cold calls efficiently & effectively (without duplicates)

## Elements of Framework
### `readRegions.py`
> reads *plz*-column from `zuordnung_plz_ort.csv`
- helper script to initially get plz's (was only relevant once - relevant list of PLZ's now in `plzList.py` - may be used/extended later)
### `plzList.py`
> file containing list of plz's generated from `readRegions.py`
- setup once & always unedited (actually rather a database then a python file)
### `data_ColdCalls.ods`
- spreadsheet to list potential contacts & document cold calls
### `ccallmaps.py`
> - starts chrome browser & searches through list of given search terms on Google Maps (after denying cookies)

- works only for German Google Maps so far (selectors given in German, because classes defined dynamically)
- super unstable

3 different versions for 3 different *systems*:
- `ccallmaps.py` (Windows)
- `ccallmaps-slow.py` (Raspberry Pi)
- `ccallmaps-slow-systemd.py` (systemd service on Raspberry Pi)

### systemd service (on Linux): `ccallmaps.service`
> [systemd service](https://github.com/torfsen/python-systemd-tutorial), which starts & restarts `ccallmaps.py` on Linux consistently when it fails

- saved in `/etc/systemd/user/ccallmaps.service` (see *usage > systemd > setup & start* below)
- meant to run *infinitely* (no auto-restart after reboot; only restart after crash of `ccallmaps.py`)

### `findFilterInfo.py`
> finds target elements from HTML files of `ccallmaps.py`-searches & writes them to CSV files with pre-sorted data & prepares it to be concatenated & filtered (by `pdMergeOnlyUnique.py`) to amend existing contacts in *searches* sheet of `data_ColdCalls.ods`

- finds Google Business Profile, website (or no website), job 
- finds job category (within medical sector (physician, alternative practitioner, healer, physio, ergo, dentist, yoga, animal, psychologist)) based on text in article & writes it in same row as respective link to Google Business Profile in CSV

#### How to `findFilterInfo.py`
> format of result sheet: *firstSheetOfListStem-lastSheetOfListStem.csv*

- move one or more search-result-HTMLs to same directory as `findFilterInfo.py`
  - **delete search results from single searches eventually!**
  - open directory in windows file explorer
    - sort files by name (ascending)
    - highlight one or more HTML files
      - **click on HTML file with biggest plz first** (bottom), then scroll to top, press+hold Shift & click HTML file with smalles plz (to highlight all files)
        > Do it that way so that smalles plz is at beginning & biggest plz at end of list in `findFilterInfo.py` later - so that output-CSV named *smallestPlz_targetGroup-biggestPlz_targetGroup.csv*
      - press CTRL+C to copy filenames
- open `findFilterInfo.py` in VSCode
  - create `fileInput` list at beginning of `findFilterInfo.py` & paste copied HTML-filenames between brackets
  - delete .html-extension from all filenames (can be done by highlighting all files using CTRL+D (several times))
  - surround all *file-stems* with quotes & place comma behind to create valid Python list

#### limitations/specifics of `findFilterInfo.py`
- needs [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc) installed on python
- currently only works if `findFilterInfo.py` in same directory as HTML files to be extracted
  - extracts to same-named CSV-files in same directory (format of resulting csv files: *originalFileStem.csv*)
- doesn't accept input; filenames (stems!) or list of them must be written to `fileInput`-variable at beginning of `findFilerInfo.py`

### `pdMergeOnlyUnique.py`
> script - merges CSV sheets into new sheet while discarding duplicate entries AND then only keep the new ones, which haven't been in the note-taking df before

#### How to `pdMergeOnlyUnique.py`
> format of result sheet: *YY-MM-DD_uniqueNew_activeSheetStem+newDataSheet*

- prepare contact-info-CSVs in same directory as `pdMergeOnlyUnique.py`
  - save *results* sheet from `data_ColdCalls.ods` as CSV (e.g. with format *YY-MM-DD_data_ColdCalls.csv*)
  - copy *firstSheetOfListStem-lastSheetOfListStem.csv* (containing filtered search results; created by `findFilerInfo.py` above) to directory of `pdMergeOnlyUnique.py`
- create file which only contains unique new contacts (which haven't been in *results* sheet of `data_ColdCalls.ods` before)
  - navigate to directory of saved files & `pdMergeOnlyUnique.py`
  - run `py pdMergeOnlyUnique.py data_ColdCalls.ods firstSheetOfListStem-lastSheetOfListStem.csv` on command line (on windows)
- open resulting csv file (saved in same directory)
  - highlight rows & columns containing data (CTRL+Shift+arrow-keys) & copy data
  - paste copied data form new file at the end of *result* sheet in active `data_ColdCalls.ods`

### tools & sources
- [zuordnung_plz_ort (CSV of regions & zip codes in Germany)](https://www.suche-postleitzahl.org/downloads)
- `requirements.txt` (ensures to install all dependencies correctly in python virtual environment)

## installation
- [install playwright](https://playwright.dev/python/docs/intro)
- create venv & install requirements ([🔗Linux](https://github.com/Sammeeey/unFollower#installation-raspberry-pi-ubuntu-desktop-22041-lts-64-bit-not-tested); [🔗Windows](https://github.com/Sammeeey/unFollower#installation-raspberry-pi-ubuntu-desktop-22041-lts-64-bit-not-tested))

## usage
### systemd
> - once systemctl service set up & running correctly -> runs until shutdown
> - following steps recommended [*python systemd* tutorial](https://github.com/torfsen/python-systemd-tutorial) in [reply of reddit question](https://www.reddit.com/r/learnpython/comments/ys9old/comment/ivxyta3/?utm_source=share&utm_medium=web2x&context=3)
> - **🛑❗basic assumption**: repository cloned into `/home/pi/Dokumente/pwmaps` of Linux (Raspberry Pi)
>   - otherwise adjustments of path's in `ccallmaps.py` & `ccallmaps.service` needed
> - using [`--user` flag on command line](https://unix.stackexchange.com/a/479977) (instead of `User=` in `ccallmaps.service`) to run user- & not system-service
>   - because setting up user-service as in [*python-systemd-tutorial*](https://github.com/torfsen/python-systemd-tutorial#creating-a-user-service) failed (because of wrong user definition or so)
>   - probably not clean solution ([difference between `--user` flag & `User=`](https://unix.stackexchange.com/a/548526/150125))

- service: `ccallmaps.service`
- systemd usage similar to [runVenv commands](https://github.com/Sammeeey/runVenv#usage)

#### setup & start
1. (`sudo apt-get install -y systemd`) (may be pre-installed on linux already)
2. `sudo nano /etc/systemd/user/ccallmaps.service` - to create *user* service (not system service as in [runVenv](https://github.com/Sammeeey/runVenv/)) (copy+paste content from `ccallmaps.service`)
2. `systemctl --user daemon-reload`
1. (`systemctl --user enable ccallmaps.service` - not relevant here because service not configured to [automatically start on reboot](https://github.com/Sammeeey/runVenv#usage))
4. `systemctl --user start ccallmaps.service`

#### debug & stop
1. `systemctl --user status ccallmaps.service`
2. `systemctl --user stop ccallmaps.service`
- `systemctl --user restart ccallmaps.service` 
- `journalctl --user-unit ccallmaps` (debug info)
- [`journalctl _PID=?????`](https://superuser.com/a/1603000) (to debug failed services)
- (`journalctl --vacuum-time=10min`) ([delete systemd log](https://unix.stackexchange.com/a/194058) -> [docs](https://freedesktop.org/software/systemd/man/journalctl.html#Commands))
  - not sure if working for systemd log of user or only for system
  - use [`sudo journalctl --rotate` instead **for now** (proably only archives the user journalctl](https://www.linuxuprising.com/2019/10/how-to-clean-up-systemd-journal-logs.html) & eventually fills up storage, but results in clean journalctl again)

### search-result-HTML's to search-result-CSV
> using `findFilterInfo.py` (see above)

### search-result-CSV's to non-duplicate-CSV (*YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv*; for amendment of *results*-sheet in `data_ColdCalls.ods`)
> using `pdMergeOnlyUnique.py` (see above)

<!-- - create *YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv* (including header)
  - save 1 *plz_targetGroup.csv* as *YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv* (name: current date & plz of latest search as *latestPlz*; **including header**)
  - open subsequent *plz_targetGroup.csv*-files in directory
    - copy all entries from *link_link* column to *Notizen* column (**without header**) & append to previously created *YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv*
- create *YY-MM-DD_presentLinks.csv* by saving *results*-sheet in `data_ColdCalls.ods` (**including all headers & explicitly using .csv format**)

- move all files (`pdMergeOnlyUnique.py`, *YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv* & *YY-MM-DD_presentLinks.csv*) to same directory
- create non-duplicate-CSV on command line
  - command line format: `pdMergeOnlyUnique.py *YY-MM-DD_presentLinks.csv* *YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv*` (creates `*YY-MM-DD_uniqueNew_YY-MM-DD_presentLinks.csv+YY-MM-DD_targetGroup_oldestPlz-latestPlz.csv`)
- copy+paste content (excluding header) from non-duplicate-CSV to end of *results*-sheet in `data_ColdCalls.ods`
  - add name of non-duplicate-CSV to line after last *link_link* in *merged file*-column of *results*-sheet in `data_ColdCalls.ods` -->

## debug info
- `.log`-file created by `ccallmaps.py` in same directory (& with same name)
  - doesn't contain `print()`-statements from `fileOperations.py`
  - doesn't contain error-messages from actual script failing errors (only the expected, catched & described one's in script) 
    - `journalctl --user-unit ccallmaps` contains info about actual errors but may need to be cleaned with from time to time (see *usage > systemd > debug & stop* above)

<!-- ### quickstart -->

### what actually happens
- Google Maps Search in Playwright (non-headless Chrome Browser on Linux Raspberry Pi)
  - based on recommended [*python systemd* tutorial](https://github.com/torfsen/python-systemd-tutorial) in [reply of reddit question](https://www.reddit.com/r/learnpython/comments/ys9old/comment/ivxyta3/?utm_source=share&utm_medium=web2x&context=3)
  - searches for certain target group along list of zip codes of Germany & saves search results as HTML's in main directory
- python programs used to extract, filter & transform relevant data (google business profile link, website, guess of job-type) into CSV format with no duplicates from different searches
  - further python programs eventually compare existing contact-data with new data & filter duplicates
- result: ongoing collection of non-duplicate contacts for e.g. cold calling

<!-- ## workflows -->

<!-- ### conventions -->

<!-- ## technologies/libraries -->

## resources
- [Raspberry Pi Setup (Ubuntu Desktop 22)](https://github.com/Sammeeey/unFollower#raspberry-pi-setup)
### libraries/frameworks
- [playwright](https://playwright.dev/python/)
- bs4
- pandas
### code
#### `ccallmaps.py`
- [Python's basic logging](https://docs.python.org/3/howto/logging.html)
  - replace all print statements with logging (maybe good practice in general)☑
  - would actually like to catch all errors by default in log file (as soon as error stops python program) - didn't find a simple enough solution yet
  - future idea: use [command line syntax to log to file automatically](https://stackoverflow.com/a/4675744) - tried - doesn't work with service normally - but may work when [explicitly called via bash](https://discourse.osmc.tv/t/redirecting-output-from-a-systemd-service-python-script-to-a-log-file/12553/6)
#### `fileOperations.py`
- build ascending list from [pathlib.Path.glob()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob) ([Python sorting basics](https://docs.python.org/3/howto/sorting.html#sorting-basics))
#### `pdMergeOnlyUnique.py`
- [concatenate pandas dataframes without duplicates](https://stackoverflow.com/a/21317570)
#### `findFilterInfo.py`
- use IGNORECASE ([py-docs 1](https://docs.python.org/3/howto/regex.html#compiling-regular-expressions), [py-docs 2](https://docs.python.org/3/library/re.html#re.IGNORECASE)) to find results independent of case
- use bs4's [`find_all(string=)`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-string-argument) along with [re.compile](https://docs.python.org/3/howto/regex.html#compiling-regular-expressions)
- [use `isinstance()` to check for type (conditionals)](https://stackoverflow.com/a/152596)
- [use `*args` parameter to accept single & multiple elements as function arguments](https://stackoverflow.com/a/998965)

### approaches
- [playwright *test generator*/*emulator* (geolocation, language, timezone)](https://playwright.dev/python/docs/codegen#emulate-geolocation-language-and-timezone)
- [delete systemd log](https://unix.stackexchange.com/a/194058)

## limitations
- slow
- region of search only determined by zip code (PLZ)

### known issues
#### logging/debugging
- `find1stfilePart()` in `fileOperations.py` just prints (& doesn't log) (so it's informations won't appear in the logs of `ccallmaps.py`)
  - potential solution: put all functions in `ccallmaps.py` (and make them all part of one class)
- don't know how to delete systemd log for user properly (raspi expected to run out of storage sooner or later, because logs probably only archived, using [`--rotate`](https://www.linuxuprising.com/2019/10/how-to-clean-up-systemd-journal-logs.html))

## potential improvements
- docs: create video examples/walk-throughs of programs & workflows
- [x] [make `ccallmaps.py` run headless on Raspberry Pi (or any other server)](https://github.com/Sammeeey/ccallmaps/commit/614d8b410e0681b9dbed50d494cac132a428cc41)
- automate further parts of the workflow (find & store HTML search results with `ccallmaps.py` & immediately convert into non-duplicate-CSV of search results)
  - move step of comparing non-duplicate search-result-CSV with active coldCall-CSV from `pdMerge_onlyUnqiue.py` as optional(?) function to `findFilterInfo.py`
  - !(easy&time-saving:) make `findFilterInfo.py` automatically create csv from all HTML files in directory (which match certain naming pattern)
- use [geo-coordinates of plz](https://www.suche-postleitzahl.org/downloads) center instead of searching for PLZs
  - [examplary Maps search, based on geo-coordinates](https://www.youtube.com/watch?v=LXKr8YRDwMc&t=226s)
- use [googlemaps API Python package](https://pypi.org/project/googlemaps/) ([docs for gmaps python package](https://googlemaps.github.io/google-maps-services-python/docs/#googlemaps.Client.places_nearby)) instead of Playwright
  - or use actual [Google Maps Nearby Places API](https://developers.google.com/maps/documentation/places/web-service/search-nearby?hl=en)
    - exmaplary [nearby business search on Google Maps](https://www.youtube.com/watch?v=YwIu2Rd0VKM&t=577s)

## results/attempts