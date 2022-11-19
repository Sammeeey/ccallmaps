# ccallmaps.py
# 22-11-13; 22:00
from fileOperations import findByCriterion, find1stfilePart
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError
from plzList import plzList

import os
import time

targetGroup = 'heilpraktiker'
# searchRegion = 'Unstruttal'
# searchRegion = 'new york city'

pathToDir = Path.cwd() / 'Dokumente' / 'pwmaps' # absolute !!Raspberry Pi!! path to directory which contains this file and all other related files
print('target directory:', pathToDir)
# change current working directory to target path (feature to make program work with systemd on linux)
os.chdir(pathToDir)
print('changed directory!? - cwd now:', pathToDir)
# ^^^^^^ACTIVATE BLOCK ON RASPBERRY PI^^^^^^ (when using with systemd) & uncomment on windows (or when using on raspberry pi manually)


def checkPageElemVisible(p, selector):
    return p.is_visible(selector)   # https://github.com/microsoft/playwright-python/issues/1513#issuecomment-1219362738



def run(playwright: Playwright, targetGroup, searchRegion) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=20000) # alll executions slowed down, so that maps doesn't just refuse to load further artciles (DOESN'T WORK: while loop seemingly regarded as one action): https://github.com/microsoft/playwright/issues/5900 & https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
    context = browser.new_context()

    page = context.new_page()
    page.set_default_timeout(120000)  # https://playwright.dev/python/docs/api/class-page#page-set-default-timeout
    
    # page.goto("https://consent.google.com/m?continue=https://www.google.com/maps&gl=DE&m=0&pc=m&uxe=eomtm&hl=de&src=1")
    page.goto("https://www.google.com/maps")

    page.get_by_role("button", name="Alle ablehnen").click()
    # page.wait_for_url("https://www.google.com/maps")

    page.get_by_role("textbox", name="In Google Maps suchen").click()
    # page.wait_for_url("https://www.google.com/maps/@52.7487019,13.2238368,14z")
    # page.wait_for_url(r"(https:\/\/www\.google\.com\/maps)\S+") # raw string notation is used to express regex in python: https://docs.python.org/3/library/re.html

    page.get_by_role("textbox", name="In Google Maps suchen").fill(f"{targetGroup} {searchRegion}")

    # page.get_by_role("textbox", name="In Google Maps suchen").press("Enter")
    page.get_by_role("button", name="Suche").click()
    # page.wait_for_url("https://www.google.com/maps/search/heilpraktiker+Unstruttal/@50.3633512,7.0269846,6z/data=!3m1!4b1")

    # page.goto("https://www.google.com/maps/search/heilpraktiker+Unstruttal/@50.3300366,6.2333588,6z")

    # infinite scroll: https://www.youtube.com/watch?v=Zk5cS7Ke3eg
    #   nth-of-type : https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type
    #       playwrights nth approach: https://playwright.dev/python/docs/selectors#n-th-element-selector
    # firstArticle = page.locator('[role="article"] >> nth=0')#.click()
    # # print(firstArticle.inner_html())  # https://playwright.dev/python/docs/api/class-locator#locator-inner-html - inspired by https://github.com/microsoft/playwright-python/issues/1284
    # a8 = page.locator('[role="article"] >> nth=7')#.click()
    # print(a8, '\n'*2, a8.inner_html())
    # # a9 = page.locator('[role="article"] >> nth=8')#.click()
    # # print(a9, '\n'*2, a9.inner_html())

    # #   scroll into view: https://playwright.dev/docs/api/class-elementhandle#element-handle-scroll-into-view-if-needed
    # a8.element_handle().scroll_into_view_if_needed()

    # # repeat for (hopefully loaded) article 16
    # a16 = page.locator('[role="article"] >> nth=15')#.click()
    # a16.element_handle().scroll_into_view_if_needed()

    # last child approach:
    noEnd = True # noEnd used to determine whether end of artcile list element was found
    while noEnd:
        lastArticle = page.locator('[role="article"] >> nth=-1')#.click()   # https://playwright.dev/python/docs/selectors#n-th-element-selector
        print(lastArticle, '\n'*2,
                # lastArticle.inner_html()    # https://playwright.dev/python/docs/api/class-locator#locator-inner-html
                )
        time.sleep(8)   # slow down python loop using time.sleep(): https://stackoverflow.com/a/16555131
        lastArticle.element_handle().scroll_into_view_if_needed()   # https://playwright.dev/docs/api/class-elementhandle#element-handle-scroll-into-view-if-needed

        # pageEndElem = page.locator('Ende der Liste')
        # pageEndElem = page.locator("span:text('Das Ende der Liste ist erreicht.')") # https://playwright.dev/python/docs/next/selectors#text-selector
        # print('\n'*2, pageEndElem)
        # # print('\n'*2, pageEndElem.inner_html())

        # noPageElem = page.locator("span:text('jiahuss878z76sgs8gzusgz')")
        # print('\n'*2, noPageElem)

        # check how many artcile elements are visible
        articleList = page.query_selector_all('[role="article"]')   # https://playwright.dev/python/docs/api/class-page#page-query-selector-all
        print(5*'\n', 'articleList length:', len(articleList), 5*'\n')
        lastArticle = page.locator('[role="article"] >> nth=-1')#.click()
        # print(lastArticle, '\n'*2, lastArticle.inner_html())
        time.sleep(6)
        lastArticle.element_handle().scroll_into_view_if_needed()

        # wait until next child respectively more children visible     https://playwright.dev/python/docs/api/class-page#page-wait-for-selector
        pageEndElem = checkPageElemVisible   # https://github.com/microsoft/playwright-python/issues/1513#issuecomment-1219362738
        try:
            pageEndElem(page, "span:text('Das Ende der Liste ist erreicht.')")
            nextArticle = page.wait_for_selector(f'[role="article"] >> nth={len(articleList)+1}', timeout=60000) # wait max 1min
        # exception based on PlaywrightTimeoutError: https://playwright.dev/python/docs/api/class-timeouterror
        except PlaywrightTimeoutError as e: # try to find most recent article (shouldn't be a problem and work quickly) - just to make sure that the problem isn't that we are actually at the end of the list but script is trying to find the next article (hence end up in infinite trail to find additional article)
            lastArticle.element_handle().scroll_into_view_if_needed()
            if pageEndElem(page, "span:text('Das Ende der Liste ist erreicht.')"):
                print('I am a pageEndElem == True error catch!')
                pass
                # --- never reached - old code below
                # print("didn't find nextArticle: ")
                # print("trying to find most recent (aka. lastArticle)...")
                # nextArticle = page.wait_for_selector(f'[role="article"] >> nth={len(articleList)}', timeout=60000) # wait max 1min
            else: # if no pageEndElem visible
                print('I am a pageEndElem not True error catch!', end='\n\n')
                print(e, end='\n\n')   # raise original error, because at that point this means that you failed to find the nextArticle for 60 seconds AND the pageEndElem isn't visible 
                print(f'FINISHED {searchRegion} without result because of TimeoutError', end='\n\n')
                with open(f'{searchRegion}_{targetGroup}_error.html', 'w') as f:   #TODO: add date & time prefix to document name   #TODO: error-file writing can actually be omitted - no point of doing it - just plz after the one of the latest successful search result file
                    f.write('please try again...:P ...or hope that pageEndElem in finally clause brings final result')
                nextArticle = page.wait_for_selector(f'[role="article"] >> nth={len(articleList)+1}', timeout=60000) # wait max 1min
        finally:
            pageEndElem(page, "span:text('Das Ende der Liste ist erreicht.')")

        
        if pageEndElem(page, "span:text('Das Ende der Liste ist erreicht.')"):
            noEnd = False
            print('end of article list')


    # # scroll results to bottom (evaluate JS) https://github.com/microsoft/playwright/issues/4302 (https://www.startpage.com/do/dsearch?query=playwright+scroll&cat=web&pl=ext-ff&language=deutsch&extVersion=1.3.0)
    # page.evaluate("() => window.scrollTo(0, document.body.scrollHeight);") https://playwright.dev/python/docs/api/class-page#page-evaluate




    # get page content (using playwright page.content): https://playwright.dev/docs/api/class-page#page-content
    pageContent = page.content()
    with open(f'{searchRegion}_{targetGroup}.html', 'w') as f:   #TODO: add date & time prefix to document name
        f.write(pageContent)

    # parse html & extract elements https://zetcode.com/python/beautifulsoup/ (https://www.startpage.com/do/dsearch?query=python+parse+html&cat=web&pl=ext-ff&language=deutsch&extVersion=1.3.0)
        

    # ---------------------
    context.close()
    browser.close()


try:
    latestSuccessPlz = find1stfilePart(fr'*_{targetGroup}.html')    # should be string: plz of first (aka. latest) [PLZ]_[TARGETGROUP].html in current working directory
    print('latest successfully saved plz:', latestSuccessPlz)
except Exception as e:
    print('The following exception occured while trying to find latestSuccessPlz:\n\n', e)


if latestSuccessPlz in plzList:
    latestPlzIndex = plzList.index(latestSuccessPlz)
    print('Latest successfully crawled plz at index:', latestPlzIndex, 'of plzList')
else: # latestSuccessPlz not in plzList
    latestPlzIndex = -1
    print("Latest plz doesn't seem to be part of plzList.\nStarting with the first plz in plzList...", end='\n\n')


if latestPlzIndex != None:
    # TODO: implement iteration of plzList starting from latestPlzIndex
    print(f'This is the element at latestPlzIndex "{latestPlzIndex}" in plzList:', plzList[latestPlzIndex])
    print(f'This is the element after latestPlzIndex (index "{latestPlzIndex+1}"):', plzList[latestPlzIndex+1])

    print('Let\'s iterate over list starting from element after latestPlzIndex until end of list')
    for plz in plzList[latestPlzIndex+1:]:
        print(f'+++++++++NEW SEARCH+++++++++\n\nSEARCHING FOR: "{targetGroup} {plz}"')
        with sync_playwright() as playwright:
            run(playwright, targetGroup=targetGroup, searchRegion=plz)

            # keep browser open by keeping python script running
            # input()
else: # if latestPlzIndex == None   # This should practically never happen (is actually not possible)...
    print("latest plz seems to be 'None'.\nPlease try again...", end='\n\n')





# TODO: handle timeout errors: https://playwright.dev/python/docs/api/class-timeouterror  &  https://playwright.dev/docs/api/class-playwright#playwright-errors

# Traceback (most recent call last):
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\pwmaps\ccallmaps4-2.py", line 135, in <module>
#     run(playwright)
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\pwmaps\ccallmaps4-2.py", line 88, in run
#     nextArticle = page.wait_for_selector(f'[role="article"] >> nth={len(articleList)+1}', timeout=60000) # wait max 1min
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\sync_api\_generated.py", line 7265, in wait_for_selector
#     self._sync(
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_sync_base.py", line 104, in _sync
#     return task.result()
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_page.py", line 368, in wait_for_selector
#     return await self._main_frame.wait_for_selector(**locals_to_params(locals()))
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_frame.py", line 317, in wait_for_selector
#     await self._channel.send("waitForSelector", locals_to_params(locals()))
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_connection.py", line 43, in send
#     return await self._connection.wrap_api_call(
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_connection.py", line 396, in wrap_api_call
#     return await cb()
#   File "C:\Users\Name\Documents\Business\3kin2\3Kin2_Heilpraktiker\coldcalls_heilpraktiker\ccallmaps\venv\lib\site-packages\playwright\_impl\_connection.py", line 78, in inner_send
#     result = next(iter(done)).result()
# playwright._impl._api_types.TimeoutError: Timeout 60000ms exceeded.
# =========================== logs ===========================
# waiting for selector "[role="article"] >> nth=71" to be visible
# ============================================================





# TODO: implement recognition of error-failed crawls -> repeat crawls if they failed
#           implement max number of repititions of crawl - if crawl failed e.g. 3 times reboot raspi - if crawl failed another 3 times e.g. send error notification to telegram (AND/OR increase timeouts)
# TODO: tests (make sure that both scripts work manually - like now - on raspi)
# TODO: connect scripts to create spreadsheet from scraped data automatically
#           standardize process (implement naming conventions for files)
# TODO: let ccallmaps.py search based on *zuordung_plz_ort* sheet
#           implement logging