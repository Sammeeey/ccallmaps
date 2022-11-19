# ccallmaps2.py
# adjustments:
#   more general url's during browser start
# 22-11-10; 19:30
from playwright.sync_api import Playwright, sync_playwright

import re
import time

targetGroup = 'carpenter'
# searchRegion = 'Unstruttal'
searchRegion = 'genf'

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=8000) # alll executions slowed down, so that maps doesn't just refuse to load further artciles (DOESN'T WORK: while loop seemingly regarded as one action): https://github.com/microsoft/playwright/issues/5900 & https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch
    context = browser.new_context()

    page = context.new_page()
    
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
    noEnd = True
    while noEnd:
        lastArticle = page.locator('[role="article"] >> nth=-1')#.click()   # https://playwright.dev/python/docs/selectors#n-th-element-selector
        print(lastArticle, '\n'*2, lastArticle.inner_html())    # https://playwright.dev/python/docs/api/class-locator#locator-inner-html
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
        print(5*'\n', 'articleList length: ', len(articleList), 5*'\n')
        lastArticle = page.locator('[role="article"] >> nth=-1')#.click()
        print(lastArticle, '\n'*2, lastArticle.inner_html())
        time.sleep(6)
        lastArticle.element_handle().scroll_into_view_if_needed()

        # wait until next child respectively more children visible     https://playwright.dev/python/docs/api/class-page#page-wait-for-selector
        try:
            nextArticle = page.wait_for_selector(f'[role="article"] >> nth={len(articleList)+1}', timeout=60000) # wait max 1min
        except:
            pass
        finally:
            pageEndElem = page.is_visible("span:text('Das Ende der Liste ist erreicht.')")   # https://github.com/microsoft/playwright-python/issues/1513#issuecomment-1219362738
        
        if pageEndElem:
            noEnd = False
            print('end of article list')
        
        # try:
        #     # find end element
        #     pass
        # except:
        #     # continue
        #     continue


    # # scroll results to bottom (evaluate JS) https://github.com/microsoft/playwright/issues/4302 (https://www.startpage.com/do/dsearch?query=playwright+scroll&cat=web&pl=ext-ff&language=deutsch&extVersion=1.3.0)
    # page.evaluate("() => window.scrollTo(0, document.body.scrollHeight);") https://playwright.dev/python/docs/api/class-page#page-evaluate




    # get page content (using playwright page.content): https://playwright.dev/docs/api/class-page#page-content
    pageContent = page.content()
    with open(f'{targetGroup}_{searchRegion}.html', 'w') as f:   #TODO: add date & time prefix to document name
        f.write(pageContent)

    # parse html & extract elements https://zetcode.com/python/beautifulsoup/ (https://www.startpage.com/do/dsearch?query=python+parse+html&cat=web&pl=ext-ff&language=deutsch&extVersion=1.3.0)
        

    # ---------------------
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)

    # keep browser open by keeping python script running
    input()


# TODO: create infinite scroll and following lines