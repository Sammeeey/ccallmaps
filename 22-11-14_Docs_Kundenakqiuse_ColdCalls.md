22-08-16
# Kundenakquise Coldcalls
## What I want
- call potential website clients systematically
    - in German-speaking regions (Germany (+ Switzerland & Austria))
    - offer web services

---------------
- unterschiedliche Zielgruppen gut möglich
    - Ärzte, Physiotherapeuten, Pensionen/Hotels, ...
    - Nach welchen *Einrichtungen* kann man Google Maps searches filtern?

## Solution 1: Semi Manual Google Search
> semi manual nearby search based on *region* column of [*zuordnung_plz_ort.csv*](https://www.suche-postleitzahl.org/downloads) & *SimpleScraper* Chrome extension (**incognito window(!!!)** - important to have uniform HTTP parameters in all links, like `?hl=de` in this case)
- list of places (businesses, locations) in Germany (Google Maps)
    - contact details (phone number + website & google maps link (if available))

## Potential Alternative Solution: GoogleMaps Places API (nearby search)
> potentially more effiecient & automated search using Google Maps API
- can basically imitate same behavior as semi manual SimpleScraper solution (using *next_page_token*)
    - see `./GMaps_API_automation`



## Documentation (Solution 1: Semi Manual Google Search)
### Initial Setup -> Done once at start of approach
> - needs to be done every time one starts new *search term* (or changes approach significantly in other way)
> - *search term* should be same in every line of *data_ColdCalls.xlsx*; if getting started with new search term, creating new *data_ColdCalls.xlsx* makes sense!

- create sheets *searches* & *results* in [data_ColdCalls.xlsx](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\data_ColdCalls.xlsx)
    - populate *results* with all results from first semi-manual SimpleScraper search approach (see below)

### Prepare Search Documentation
- open *data_ColdCalls.xlsx* (which includes copy of [*zuordnung_plz_ort.csv*](https://www.suche-postleitzahl.org/downloads) (plz sorted descending))
    - open sheet *searches*
        - click on line number of last search (to highlight line)
        - copy line & paste below (*region* get's updated automatically with next *region* entry from sheet *zuordnung_plz_ort.csv* due to reference formula)
            - maybe update *date* in new line (format: YY-MM-DD)
            - copy *region* cell of new line

### Google Maps Search
- open [Google Maps](https://maps.google.com) in **incognito window(!!!)** of Chrome Browser
- paste content of previously copied *region* cell in search bar
- copy latest *search term* from *data_ColdCalls.xlsx*'s sheet *searches* & search
    > *search term* should actually be same in every line; if getting started with new search term, creating new *data_ColdCalls.xlsx* makes sense!
- **make sure that links have `?hl=de` as HTTP parameter in URL**
  - hover over any search result (business) & see that end of URL contains `?hl=de` (not `?hl=en`)

### SimpleScraper
<!-- - scroll all results in left sidebar manually until *Das Ende der Liste ist erreicht.* (or equivalent in different language) displayed -->
- scroll all results in left sidebar manually until *You've reached the end of the list.* (or equivalent in different language) displayed
- click on *Extentions* button in upper left corner of Chrome Browser (**incognito window(!!!)**)
    - click *launch SimpleScraper*
    - click *scrape this website* in SimpleScraper popup
- click plus-icon in upper left corner to *Add a property* (property name: *link*)
- navigate cursor to *selector...* field below property name field
- switch to *data_ColdCalls.xlsx*'s sheet *searches* & copy latest *selector* (should be same in every line)
    > selects only links to Google Maps entries in Google Maps Search results: `[role=article] a[href^="https://www.google.com/maps"]`
- switch back to Google Maps & paste copied *selector* (expected: *120 items selected* (highlighted green) by SimpleScraper, if enough results and scrolled until end of list)
- click tick☑ button next to property name of SimpleScraper, to save property
- click *VIEW RESULTS* on upper right of SimpleScraper interface
- find preview of results in new tab (expected: 120 rows, 120 properties, table preview with *link* and *link_link* column + respective JSON preview)
- click *Download CSV* button
    - save in [*semiManualSearch* folder](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach) (format: YY-MM-DD_region.csv) (may switch to sheet *searches* in *data_ColdCalls.xlsx*, copy & paste)
        > **IMPORTANT** naming convention: no white space! if white space in region names connect with `_` (underscore)
- click *Download JSON* button
    - save in [*semiManualSearch* folder](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach) (format: YY-MM-DD_region.json) (may use previously saved csv of same search & change *.csv* suffix to *.json*)
> saved CSV and JSON serve as backup (in case of messed up csv's during following merge)
- copy previously saved CSV to sub-directory [*mergePy*](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\mergePy)

### Prepare Extraction of new, unique Entries
- switch to *data_ColdCalls.xlsx*'s sheet *results*
    - click character of *link_link* column (= select column) & copy content
- open new spreadsheet (CTRL+N) & paste *link_link* data
    - save as csv in [*mergePy* directory](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\mergePy) (format: *YY-MM-DD_presentLinks.csv*)
<!-- 22-11-04 -->
    - **IMPORTANT**: really save in CSV format (using Libre Office; not only with `.csv` extension)

### Extract unique Entries (Python Script: CLI)
- open terminal (cmder) & navigate to *mergePy* directory: `cd C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\mergePy`
<!-- ### create initial csv with data from two searches, but without duplicates (SUPERFLUOUS! Just take the first csv as start point, then run the second one with *pdMerge_onlyUnique.py* against it)
`py pdMerge.py 22-08-16_Körner.csv 22-08-16_Mühlhausen.csv`
- expects two csv's with gmaps links in a *link_link* column (provided by SimpleScraper (see above))
    - csv's must be in same (current) directory as *pdMerge.py* -->

#### Option 1: Merge one new region file
- execute Python script *pdMerge_onlyUnique.py* with previously created csv's as command line aguments
    1. *YY-MM-DD_presentLinks.csv*
    2. *YY-MM-DD_region.csv*
    > also possible: copy content from many region searches together in one new csv file; then run new csv instead of *YY-MM-DD_region.csv*
    >
    > possible because `pdMerge_onlyUnique.py` drops all duplicates (not only those of comparison between file, but also within file itself)

<!-- DON'T TO THAT!!! You lose data entries that way, because pdMerge_onlyUnique.py doesn't only drop duplicates but ALSO DROPS ALL REMAINING ENTRIES WHICH HAVE ALREADY BEEN IN THE FIRST FILE BEFORE!!!! -->
<!-- #### Option 2: Merge several new region files
- create csv which conatains only entries (from new search), which aren't included in previous csv already
`py pdMerge_onlyUnique.py 22-08-16_merged_22-08-16_Körner.csv+22-08-16_Mühlhausen.csv 22-08-16_Mühlhausen.csv` -->

<!-- 22-11-04 -->
### Add new unique entries to existing cold call sheet
> preparation: create backup copy of existing `data_ColdCalls.xlsx` by creating copy of file and adding date at the beginning (exmaple: `22-11-09_data_ColdCalls.xlsx`)
- switch *results* in [data_ColdCalls.xlsx](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\data_ColdCalls.xlsx)
  - go to end of list (go to `link_link` column & press CTRL+down arrow to jump to end of list)
- navigate to `date` column in next line & enter date (if new day)
- in `merged file` column enter name of file with new unique links (from previously conducted commandline merge)
    > example: `22-11-04_uniqueNew_22-11-04_presentLinks.csv+22-11-04_Südeichsfeld.csv`
- copy all links from merged file
  - navigate to first link in `link_link` column of merged file 
  - press CTRL+Shift+down arrow (to highlight all links in column)
  - press CTRL+C (to copy all highlighted links)
- switch *results* in [data_ColdCalls.xlsx](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\data_ColdCalls.xlsx)
  - paste copied links into first empty line in `link_link` column (CTRL+V) 


## CALL PEOPLE!
> - using script

- open *results* in [data_ColdCalls.xlsx](C:\Users\Name\Documents\Business\Samuel Hartmann\ColdCall_Webservices\semiManualSeach\data_ColdCalls.xlsx)
- copy+paste & open maps link to browser window
- after done with calling write `go on here` in `merged file` column after last called person









<!-- superfluous! don't need clickable links - copy+paste with keyboard shortcuts is quicker -->
<!-- ## Libre Calc
### [find & replace to generate clickable links](https://ask.libreoffice.org/t/calc-convert-text-to-link/1945/2)
- find: `(https).*`
- replace: `=HYPERLINK("&")`
<!-- - new find (to omit cells which already contain *=HYPERLINK*): (?=(https.*))(?<!(=HYPERLINK\("))
    - based on: ["and" expression](https://stackoverflow.com/a/469951) & [negative lookbehind](https://stackoverflow.com/a/3194883) -->
 -->


---------------

## Copy & Paste Resources
### SimpleScraper Selector
- `[role=article] a[href^="https://www.google.com/maps"]` (selects only links to Google Maps entries in Google Maps Search results)


---------------
## There is certainly an easier & more straight forward ways to filter duplicates in .ods sheets...