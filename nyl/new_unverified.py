# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

# [Documentation - Summary] Tests user workflow of successful
# registration with valid SSN4 and OTP pass
# For use with Entry Info file version: nyl02192020.txt

# The test case ex is inherited from unittest.TestCase.
# Inheriting from TestCase class is the way to tell unittest module that this is a test case.
class NYlotto(confTest.NYlottoBASE):
    

# This is the test case method. The test case method should always start with the characters test.
# The first line inside this method creates a local reference to the driver object created in setUp method.
    def test_newUnverified(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail
        print(testemail)
        try:
                funct.purge(self, testemail)
                print('test user purged')
        except:
                print('no test user found')
# Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-2400
        driver = self.driver
# opens local file with user data
        notepadfile = open('/Users/Shared/testing/nyl02192020.txt', 'r')
# variable for each line in the file
        entry_info = notepadfile.read().splitlines()
# The driver.get method will navigate to a page given by the URL.
# WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
# before returning control to your test or script.
        driver.get(self.url)
# Assertion that the title has Single Sign On in the title.
        self.assertIn("Single Sign On", driver.title)

# Instructions for webdriver to read and input user data via the info on the .txt doc.
        funct.waitAndSend(driver, var.regV.fname, entry_info[0])
        funct.waitAndSend(driver, var.regV.lname, entry_info[1])
        funct.waitAndSend(driver, var.regV.housenum, entry_info[2])
        funct.waitAndSend(driver, var.regV.street, entry_info[3])
        funct.waitAndSend(driver, var.regV.city, entry_info[4])
# Find and select the state according to the info in the .txt doc
# Uses a for loop to iterate through the list of states until element
# matches the entry info in the text file. Then clicks the element found.
        select_box = driver.find_element_by_name("state")
        funct.waitAndClick(driver, var.regV.state_dropdown)
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text in entry_info[5]:
                element.click()
                break
        funct.waitAndSend(driver, var.regV.zip, entry_info[6])
        funct.waitAndSend(driver, var.regV.phone, '5168675309')
        funct.waitAndSend(driver, var.regV.ssn4, entry_info[8])
        funct.waitAndSend(driver, var.regV.dob, (entry_info[9] + entry_info[10] + entry_info[11]))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
        funct.waitAndSend(driver, var.regV.password, entry_info[12])
        funct.waitAndSend(driver, var.regV.confirmPsw, entry_info[12])
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)
# 2nd screen. OTP selection screen
        funct.waitAndClick(driver, var.otpV.text_button)
        print("Test complete, usewr created")

# Boiler plate code to run the test suite
if __name__ == "__main__":
    #First runner will enable html logs on your current directory, second runner will keep local console logs
    ###unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    unittest.main()