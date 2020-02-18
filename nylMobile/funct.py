# [Documentation - Setup] This section lists all dependencies
# that are imported for function file to work
from selenium import webdriver
import unittest, time, re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import util
from selenium.webdriver import ActionChains

# [Documentation - Summary] This file creates the functions for
# use in the automation test suite of NYL SSO

# [Documentation - Function] Webdriver uses actionchains to  wait for a specified page element
# to appear prior to the next interaction on the page
def waitUntil(browser, elem):
    a = ActionChains(browser)
    try:
        a.move_to_element(browser.find_element(elem[0], elem[1])).perform()
        assert(browser.find_element(elem[0], elem[1]))
    except:
        time.sleep(2)
        try:
            a.move_to_element(browser.find_element(elem[0], elem[1])).perform()
            assert(browser.find_element(elem[0], elem[1]))
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

def actionSend(browser, keys):
    a = ActionChains(browser)
    a.send_keys(keys)
    a.perform()


# [Documentation - Function] Function that grabs UTC time and converts to human readable format
def timeStamp():
    ts = time.gmtime()
    times = time.strftime("%Y-%m-%d_%H-%M-%S", ts)
    return times

# [Documentation - Function] Function that checks the text of a given element against a given stub
def checkText(browser, elem, stub):
    waitUntil(browser, elem)
    el = browser.find_element(elem[0], elem[1])
    if el.text == stub:
        assert el.text == stub
    else:
        print('E---Text Incorrect!\n\nExpected text: "' + stub + '"\n\n but text was: "' + el.text + '"')
        assert el.text == stub

# # [Documentation - Function] Function that calls the script to grab full page UTC timestamped screenshot
# def fullshot(self):
#     self.driver.set_window_position(0, 0)
#     self.driver.maximize_window()
#     timestamp = timeStamp() + '.png'
#     util.fullpage_screenshot(self.driver, timestamp)
