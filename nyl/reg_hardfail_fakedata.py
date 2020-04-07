# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

# [Documentation - Summary] Tests user workflow of failed
# registration with fake data

class NYlotto(confTest.NYlottoBASE):

# Checks that user is redirected to Hard Fail screen when fake data is submitted
    def test_regHardFailFakeData(self):
# Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-1922
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.url)
        # putting in acceptable but invalid data
        funct.waitAndSend(driver, var.regV.fname, "Fake")
        funct.waitAndSend(driver, var.regV.lname, "Test")
        funct.waitAndSend(driver, var.regV.housenum, "12345")
        funct.waitAndSend(driver, var.regV.street, "First Street")
        funct.waitAndSend(driver, var.regV.city, "Anytown")
        funct.waitAndClick(driver, var.regV.state_dropdown)
        driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(10) > div > select > option:nth-child(2)").click()
        funct.waitAndSend(driver, var.regV.zip, "11223")
        funct.waitAndSend(driver, var.regV.phone, "5559876543")
        funct.waitAndSend(driver, var.regV.ssn4, "1234")
        funct.waitAndSend(driver, var.regV.dob, "01/01/1990")
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, self.testemail)
        funct.waitAndSend(driver, var.regV.password, "Test1234")
        funct.waitAndSend(driver, var.regV.confirmPsw, "Test1234")
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)

        # checking that we get to the "can not verify your identity" screen
        try:
            driver.find_elements_by_class_name("migration-failed-body")
        except:
            print("Can not find 'Identity verification failed' screen")
        if "Sorry, we cannot verify your identity." in driver.page_source:
             print("PASS - 'Identity verification failed' screen reached.")
        elif driver.find_elements_by_name("q") != []:
            print("FAIL - Reached successful registration and redirected to callback uri (Google.com)")
            funct.fullshot(driver)
            try:
                funct.purge(self, self.testemail)
                print('test user purged')
            except:
                print('no test user found')
            raise Exception('Registration succeeded where it was supposed to fail.')
        else:
            print("FAIL - Neither Identity verification failed screen nor Registration successful screen reached.")
            funct.fullshot(driver)
            try:
                funct.purge(self, self.testemail)
                print('test user purged')
            except:
                print('no test user found')
            raise Exception('Registration redirected incorrectly.')
# Deleting test data
        try:
            funct.purge(self, self.testemail)
            print('E-- test user was created but was purged')
        except:
            pass

# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    # unittest.main(warnings='ignore')