# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, confTest, HTMLTestRunner   #Custom class for NYL

class NYLadmin(confTest.NYLadminBASE):

# Checks login with correct email & password redirects successfully
    def test01_loginSuccess(self):
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.url)

        # Instructions for webdriver to read and input user data via the info on the .txt doc.
        # Credentials are localized to one instance via the var file
        funct.waitAndSend(driver, var.loginV.email, var.CREDSadmin.superadmin_username)
        funct.waitAndSend(driver, var.loginV.password, var.CREDSadmin.superadmin_psw)
        funct.waitAndClick(driver, var.loginV.signin_button)
        time.sleep(1)
        # Successful login should redirect to dashboard home page.
        # Checking that the home breadcrumb button is present on page.
        if driver.find_elements_by_xpath(var.homeDashV.home_breadcrumb_link[1]) != []:
            print('PASS - login successful and redirected to Dashboard home')
        else:
            funct.fullshot(driver)
            print('FAIL - Login attempt failed or redirected incorrectly')
            raise Exception('Unexpected behavior encountered')

# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    # unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    unittest.main(warnings='ignore')