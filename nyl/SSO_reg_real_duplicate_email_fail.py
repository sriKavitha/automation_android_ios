# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

# The test case class is inherited from unittest.TestCase.
# Inheriting from TestCase class is the way to tell unittest module that this is a test case.
class NYlotto(confTest.NYlottoBASE):

# This is the test case method. The test case method should always start with the characters test.
# The first line inside this method creates a local reference to the driver object created in setUp method.
    def test_01_regDupeEmail(self):
        # Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-1923
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
        # Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-1923
        print("\nChecks for failed registration with duplicate email in userpool")
        testemail = self.testemail
        driver = self.driver
        print('\n----------\n' + 'Test setup')
        # creates a verified user with valid SSN4
        funct.createVerifiedUser(self, testemail)
        print('----------')
        # Switch to blank registration page
        driver.get(self.reg_url)
        # Assertion that the title has Single Sign On in the title.
        self.assertIn("Single Sign On", driver.title)

        # Instructions for webdriver to read and input user data via the info on the .txt doc.
        # Credentials are localized to one instance via the var file
        funct.waitAndSend(driver, var.regV.fname, var.credsSSOWEB.fname)
        funct.waitAndSend(driver, var.regV.lname, var.credsSSOWEB.lname)
        funct.waitAndSend(driver, var.regV.housenum, var.credsSSOWEB.housenum)
        funct.waitAndSend(driver, var.regV.street, var.credsSSOWEB.street)
        funct.waitAndSend(driver, var.regV.city, var.credsSSOWEB.city)
        # Find and select the state according to the info in the .txt doc
        # Uses a for loop to iterate through the list of states until element
        # matches the entry info in the text file. Then clicks the element found.
        select_box = driver.find_element_by_name("state")
        funct.waitAndClick(driver, var.regV.state_dropdown)
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text in var.credsSSOWEB.state:
                element.click()
                break
        funct.waitAndSend(driver, var.regV.zip, var.credsSSOWEB.zip)
        funct.waitAndSend(driver, var.regV.phone, "5552221234")
        funct.waitAndSend(driver, var.regV.ssn4, var.credsSSOWEB.ssn4)
        funct.waitAndSend(driver, var.regV.dob,
                          (var.credsSSOWEB.dob_month + var.credsSSOWEB.dob_date + var.credsSSOWEB.dob_year))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
        funct.waitAndSend(driver, var.regV.password, var.credsSSOWEB.password)
        funct.waitAndSend(driver, var.regV.confirmPsw, var.credsSSOWEB.password)
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)
        # Checking that error message appears and registration does not proceed.
        warning = driver.find_element(var.regV.submit_button_error[0], var.regV.submit_button_error[1])
        if funct.checkErrorText(driver, var.regV.submit_button_error, var.regV.duplicateEmailErrorStub) == True:
            print('PASS - Error warnings found and warning copy is correct')
            print('Warning text displayed is "' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.regV.submit_button_error, var.regV.duplicateEmailErrorStub) == False:
            try:
                funct.purgeSSOemail(self, testemail)
                print('test user purged')
            except:
                print('no test user found')
            print(
                'FAIL - Warning should say "' + var.regV.duplicateEmailErrorStub + '" , but says "' + warning.get_attribute(
                    "innerText") + '"!')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')
        else:
            try:
                funct.purgeSSOemail(self, testemail)
                print('test user purged')
            except:
                print('no test user found')
            print("E---Error message did not appear or other unexpected behavior. Test Failed.")
            funct.fullshot(driver)
            raise Exception('Unexpected message or behavior.')
        # Deleting test data
        print('\n----------\n' + 'Test complete!\n\nTest clean up commencing')
        try:
            funct.purgeSSOemail(self, testemail)
        except:
            pass
        print('----------')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))