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

# Checks main error appears when empty form is submitted
    def test01_loginError(self):
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

# Checks main error copy
    def test02_loginErrorCopy(self):
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndClick(driver, var.loginV.login_button)
        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == True:
            print('PASS - Warning copy text is correct')
            print('Warning text displayed is " ' + warning.get_attribute("innerText") + ' "')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.loginErrorStub + '" , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')

# Checks mandatory field errors are found
    def test03_loginRequiredErrors(self):
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
            print('PASS - Error warnings found and present')
        elif len(warningList) > 0:
            print('FAIL - ')
            print(warningList)
            print(' Error warning(s) missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')

# Checks mandatory field error copy
    def test04_loginRequiredErrorsCopy(self):
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
            if funct.checkErrorText(driver, warning, var.loginV.requiredErrorStub) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print('PASS - Error warnings found and copy is correct')
        elif len(warningList) > 0:
            print('FAIL - ')
            print(warningList)
            print('Error warning(s) copy is incorrect')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')

# Checks missing email login attempt error
    def test05_loginIncompleteEmailError(self):
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
            print('Warning text displayed is " ' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say " ' + var.loginV.loginErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')

# Checks missing password login attempt error
    def test06_loginIncompletePswError(self):
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
            print('PASS - Warning copy text is correct')
            print('Warning text displayed is "' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.loginErrorStub) == False:
            print('FAIL - Warning should say " ' + var.loginV.loginErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect')

# Checks that invalid email input displays error
    def test07_loginInvalidEmailError(self):
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, "bademail$$$%%%rosedigital")
        funct.waitAndClick(driver, var.loginV.login_button)
        if funct.checkError(driver, var.loginV.email_error) == True:
            print('PASS - "' + var.loginV.email_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.email_error) == False:
            print('FAIL - "' + var.loginV.email_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')

# Checks that invalid email input displays correct error message
    def test08_loginInvalidEmailErrorCopy(self):
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, "bademail$$$%%%rosedigital")
        funct.waitAndClick(driver, var.loginV.login_button)

        warning = driver.find_element(var.loginV.email_error[0], var.loginV.email_error[1])
        if funct.checkErrorText(driver, var.loginV.email_error, var.loginV.emailErrorStub) == True:
            print('PASS - Error warnings found and copy is correct')
            print('Warning text displayed is "' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.loginV.email_error, var.loginV.emailErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.emailErrorStub + ' , but says "' + warning.get_attribute("innerText") + '"')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')


# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    # unittest.main(warnings='ignore')