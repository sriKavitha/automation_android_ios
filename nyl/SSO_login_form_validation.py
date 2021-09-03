# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

class NYlotto(confTest.NYlottoBASE):

    def test_01_loginError(self):
        testenv = self.env
        print("\nTESTING " + testenv + " ENVIRONMENT")
        print("\nChecks main error appears when empty form is submitted and text copy is correct")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndClick(driver, var.loginV.login_button)
        if funct.checkError(driver, var.loginV.login_button_error) == True:
            print('PASS - ' + var.loginV.login_button_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.login_button_error) == False:
            print('FAIL - ' + var.loginV.login_button_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')
        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == True:
            print('PASS - Warning copy is correct')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.loginErrorStub + '" , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')
        print('----------')
        funct.closeWindow(driver, 'New York Lottery - Single Sign On')

    def test_02_loginRequiredErrors(self):
        print("\nChecks mandatory field errors are found and text copy is correct")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndClick(driver, var.loginV.email)
        funct.waitAndClick(driver, var.loginV.password)
        funct.waitAndClick(driver, var.loginV.login_button)
        warningList = []
        # These are the CSS selectors for the 2 red text error elements
        warningsExpected = [var.loginV.email_error, var.loginV.password_error]
        for warning in warningsExpected:
            if funct.checkError(driver, warning) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print('PASS - Error warnings present')
        elif len(warningList) > 0:
            print('FAIL - ')
            print(warningList)
            print(' Error warning(s) missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')
        warningsExpected = [var.loginV.email_error, var.loginV.password_error]
        for warning in warningsExpected:
            if funct.checkErrorText(driver, warning, var.loginV.requiredErrorStub) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print('PASS - Error warnings copy is correct')
        elif len(warningList) > 0:
            print('FAIL - ')
            print(warningList)
            print('Error warning(s) copy is incorrect')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')
        print('----------')
        funct.closeWindow(driver, 'New York Lottery - Single Sign On')

    def test_03_loginIncompleteEmailError(self):
        print("\nChecks missing email login attempt error and text copy is correct")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.password, "valid1234")
        funct.waitAndClick(driver, var.loginV.login_button)
        if funct.checkError(driver, var.loginV.login_button_error) == True:
            print('PASS - ' + var.loginV.login_button_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.login_button_error) == False:
            print('FAIL - ' + var.loginV.login_button_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')

        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == True:
            print('PASS - Warning copy text is correct')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say " ' + var.loginV.loginErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')
        print('----------')
        funct.closeWindow(driver, 'New York Lottery - Single Sign On')

    def test_04_loginIncompletePswError(self):
        print("\nChecks missing password login attempt error and text copy is correct")
        testemail = self.testemail
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, testemail)
        funct.waitAndClick(driver, var.loginV.login_button)
        if funct.checkError(driver, var.loginV.login_button_error) == True:
            print('PASS - ' + var.loginV.login_button_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.login_button_error) == False:
            print('FAIL - ' + var.loginV.login_button_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')

        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == True:
            print('PASS - Warning copy is correct')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say " ' + var.loginV.loginErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')
        print('----------')
        funct.closeWindow(driver, 'New York Lottery - Single Sign On')

    def test_05_loginInvalidEmailError(self):
        print("\nChecks that invalid email input displays error and text copy is correct")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, "bademail$$$%%%rosedigital")
        funct.waitAndClick(driver, var.loginV.login_button)
        if funct.checkError(driver, var.loginV.email_error) == True:
            print('PASS - ' + var.loginV.email_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.email_error) == False:
            print('FAIL - "' + var.loginV.email_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')
        warning = driver.find_element(var.loginV.email_error[0], var.loginV.email_error[1])
        if funct.checkErrorText(driver, var.loginV.email_error, var.loginV.emailErrorStub) == True:
            print('PASS - Error warnings copy is correct')
        elif funct.checkErrorText(driver, var.loginV.email_error, var.loginV.emailErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.emailErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')
        print('----------')
        funct.closeWindow(driver, 'New York Lottery - Single Sign On')


# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    # unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    unittest.main(warnings='ignore')