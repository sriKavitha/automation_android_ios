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

# Checks that incorrect email login attempt displays error
    def test01_loginIncorrectEmailError(self):
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, "notarealemail@rosedigital.co")
        funct.waitAndSend(driver, var.loginV.password, "Test1234")
        funct.waitAndClick(driver, var.loginV.login_button)
        # checks if error message is present
        if funct.checkError(driver, var.loginV.login_button_error) == True:
            print('PASS - ' + var.loginV.login_button_error[2] + ' is present.')
        elif funct.checkError(driver, var.loginV.login_button_error) == False:
            print('FAIL - ' + var.loginV.login_button_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')

# Checks that incorrect email login attempt displays correct error message
    def test02_loginIncorrectEmailErrorCopy(self):
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, "notarealemail@rosedigital.co")
        funct.waitAndSend(driver, var.loginV.password, "Test1234")
        funct.waitAndClick(driver, var.loginV.login_button)
        # checks if error text matches recorded copy
        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.badEmailErrorStub) == True:
            print('PASS - Error warnings found and warning copy is correct')
            print('Warning text displayed is "' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.badEmailErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.badEmailErrorStub + '" , but says "' + warning.get_attribute("innerText") + '"!')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')

# Checks that incorrect password login attempt displays error
    def test03_loginIncorrectPswError(self):
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
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
            print('PASS - registration successful and redirected to callback uri')
        else:
            funct.fullshot(driver)
            print('FAIL - registration redirect screen not reached. Test can not proceed')
        # create new driver instance for login session
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, testemail)
        funct.waitAndSend(driver, var.loginV.password, "badpassword")
        funct.waitAndClick(driver, var.loginV.login_button)
        # checks if error message is present
        if funct.checkError(driver, var.loginV.login_button_error) == True:
            print('PASS - ' + var.loginV.login_button_error[2] + ' is present')
        elif funct.checkError(driver, var.loginV.login_button_error) == False:
            print('FAIL - ' + var.loginV.login_button_error[2] + ' is missing')
            funct.fullshot(driver)
            raise Exception('Error warning element not found')
        # Deleting test data
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')
        print('Test complete!')

# Checks that incorrect password login attempt displays correct error message
    def test04_loginIncorrectPswErrorCopy(self):
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
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
            print('PASS - registration successful and redirected to callback uri')
        else:
            funct.fullshot(driver)
            print('FAIL - registration redirect screen not reached. Test can not proceed')

        # create new driver instance for login session
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.login_url)
        # triggering error
        funct.waitAndSend(driver, var.loginV.email, testemail)
        funct.waitAndSend(driver, var.loginV.password, "badpassword")
        funct.waitAndClick(driver, var.loginV.login_button)
        # checks if error text matches recorded copy
        warning = driver.find_element(var.loginV.login_button_error[0], var.loginV.login_button_error[1])
        if funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.badPasswordErrorStub) == True:
            print('PASS - Error warnings found and warning copy is correct')
            print('Warning text displayed is "' + warning.get_attribute("innerText") + '"')
        elif funct.checkErrorText(driver, var.loginV.login_button_error, var.loginV.badPasswordErrorStub) == False:
            print('FAIL - Warning should say "' + var.loginV.badPasswordErrorStub + '" , but says "' + warning.get_attribute("innerText") + '"!')
            funct.fullshot(driver)
            raise Exception('Error warning(s) copy is incorrect')
        # Deleting test data
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')
        print('Test complete!')

# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
    # unittest.main(warnings='ignore')