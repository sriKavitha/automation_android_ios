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

# Checks login with correct email & password redirects successfully
    def test01_loginSuccess(self):
        # creates a verified user with valid SSN4
        testemail = self.testemail
        # Check for existing test user and wipe it from userpool prior to test execution
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.url)

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
        # for future use with mobile phone code grabber
        # if self.env == 'dev':
        #     funct.waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        # elif self.env == 'qa':
        #     funct.waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        # elif self.env == 'stage':
        #     funct.waitAndSend(driver, var.regV.phone, self.testphone2)
        funct.waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        funct.waitAndSend(driver, var.regV.ssn4, var.credsSSOWEB.ssn4)
        funct.waitAndSend(driver, var.regV.dob,
                          (var.credsSSOWEB.dob_month + var.credsSSOWEB.dob_date + var.credsSSOWEB.dob_year))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
        funct.waitAndSend(driver, var.regV.password, var.credsSSOWEB.password)
        funct.waitAndSend(driver, var.regV.confirmPsw, var.credsSSOWEB.password)
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)
        # 2nd screen. OTP selection screen
        funct.waitAndClick(driver, var.otpV.text_button)
        # 3rd screen. OTP code entry screen
        # for future use with mobile phone code grabber
        # if self.env == 'dev':
        #     funct.waitAndSend(driver, var.otpV.otp_input, "111111")
        # elif self.env == 'qa':
        #     funct.waitAndSend(driver, var.otpV.otp_input, "111111")
        # elif self.env == 'stage':
        #     # wait for phone code to be received by real device & input into field
        #     pass
        funct.waitAndSend(driver, var.otpV.otp_input, "111111")
        funct.waitAndClick(driver, var.otpV.otp_continue_button)
        time.sleep(5)
        # 4th screen. Successful registration should redirect to Google.com.
        # Checking that the search field on google.com is present on page.
        if driver.find_elements_by_name("q") != []:
            print('Initial registration successful.')
        else:
            funct.fullshot(driver)
            print('FAIL - Initial registration redirect screen not reached. Test can not proceed')
            raise Exception('Registration redirected incorrectly')

        # create new driver instance for login session
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # Login attempt
        funct.waitAndSend(driver, var.loginV.email, testemail)
        funct.waitAndSend(driver, var.loginV.password, var.credsSSOWEB.password)
        funct.waitAndClick(driver, var.loginV.login_button)
        # Successful login should redirect to Google.com.
        # Checking that the search field on google.com is present on page.
        if driver.find_elements_by_name("q") != []:
            print('PASS - login successful and redirected to callback uri')
        else:
            funct.fullshot(driver)
            print('FAIL - Login attempt failed or redirected incorrectly')
            raise Exception('Unexpected behavior encountered')
        # Deleting test data
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')
        print("Test complete!")

# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    # unittest.main(warnings='ignore')