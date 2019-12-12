# [Documentation - Setup] This section lists all dependencies
# that are imported for function file to work
from selenium import webdriver
import unittest, time, re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# [Documentation - Summary] This file creates the functions for
# use in the automation test suite of NYL SSO

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