# [Documentation - Setup] This section lists all dependencies
# that are imported for function file to work
from browsermobproxy import Server
from selenium import webdriver
import unittest, time, re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os, json, util
from urllib.parse import urlparse

# [Documentation - Summary] This file creates the functions for
# use in the automation test suite of NYL SSO

def generateHAR(server, driver):
    hurl = str(driver.current_url)
    server = Server("/Users/browsermob-proxy-2.1.4/bin/browsermob-proxy",  options={'port': 8090})
    server.start()
    proxy = server.create_proxy()
    chromedriver = "/usr/local/bin/chromedriver"
    url = urlparse(proxy.proxy).path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(url))
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    proxy.new_har("test", options={'captureHeaders': True})
    driver.get(hurl)
    result = json.dumps(proxy.har, ensure_ascii=False)
    print(result)
    harname = str('HAR_' + timeStamp())
    with open(harname, 'w') as har_file:
        json.dump(proxy.har, har_file)
    proxy.close()

# [Documentation - Function] Webdriver waits for a specified page element
# to appear prior to the next interaction on the page
def waitUntil(browser, elem):
    try:
        browser.find_element(elem[0], elem[1])
    except:
        try:
            browser.find_element(By.elem)
        except:
            print("E--" + elem[1] + " elem not found")

# [Documentation - Function] Webdriver waits for a specified page element
# to appear and then proceeds to click on it
def waitAndClick(browser, elem):
    waitUntil(browser, elem)
    browser.find_element(elem[0], elem[1]).click()

# [Documentation - Function] Webdriver waits for a specified page element
# to appear and then proceeds to send keys to it
def waitAndSend(browser, elem, keys):
    waitUntil(browser, elem)
    browser.find_element(elem[0], elem[1]).send_keys(keys)

# [Documentation - Function] Function that grabs UTC time and converts to human readable format
def timeStamp():
    ts = time.gmtime()
    times = time.strftime("%Y-%m-%d_%H-%M-%S", ts)
    return times

# [Documentation - Function] Function that calls the script to grab full page UTC timestamped screenshot
def fullshot(browser):
    browser.set_window_position(0, 0)
    browser.maximize_window()
    timestamp = timeStamp() + '.png'
    util.fullpage_screenshot(browser, timestamp)

# [Documentation - Function] Checks that an error exists
def checkError(browser, elemWarning):
    try:
        browser.find_element(elemWarning[0], elemWarning[1])
        return True
    except:
        return False

# [Documentation - Function] Checks the actual warning text against the reported warning copy
def checkErrorText(browser, elemWarning, elemWarningStub):
    warning = browser.find_element(elemWarning[0], elemWarning[1])
    if warning.get_attribute("innerText") == elemWarningStub:
        return True
    else:
        return False


# [Documentation - Function] Checks the actual value in the field against the expected value
def checkValue(browser, elem, valueExpected):
    warning = browser.find_element(elem[0], elem[1])
    if warning.get_attribute("value") == valueExpected:
        return True
    else:
        return False
