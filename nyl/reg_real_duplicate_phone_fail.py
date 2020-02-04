# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util                             #Custom class for NYL

# [Documentation - Summary] Tests user workflow of failed
# registration with duplicate phone in database
# For use with Entry Info file version: nyl01072020.txt

# [Documentation - Variables] Test file specific variables
#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"
url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
testemail = "marie.liao+ssotest@rosedigital.co"
testemail2 = "marie.liao+ssotest2@rosedigital.co"

# The test case class is inherited from unittest.TestCase.
# Inheriting from TestCase class is the way to tell unittest module that this is a test case.
class NYlotto(unittest.TestCase):

# The setUp is part of initialization, this method will get called before every test function which you
# are going to write in this test case class. Here you are creating the instance of Chrome WebDriver.
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        # self.driver = webdriver.Remote(
        #    command_executor='http://192.168.86.26:4444/wd/hub',
        #    desired_capabilities= {
        #        "browserName": "chrome",
        #        "version": "",
        #        "platform": "ANY",
        #        "javascriptEnabled": True,
        #        'chromeOptions': {
        #            'useAutomationExtension': False,
        #            'args': ['--disable-infobars']
        #        }
        #   })
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(12)
        self.verificationErrors = []
        self.accept_next_alert = True

# This is the test case method. The test case method should always start with the characters test.
# The first line inside this method creates a local reference to the driver object created in setUp method.
    def test_reg1(self):
        driver = self.driver
# opens local file with user data
        notepadfile = open('/Users/nyl01072020.txt', 'r')
# variable for each line in the file
        entry_info = notepadfile.read().splitlines()
# The driver.get method will navigate to a page given by the URL.
# WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
# before returning control to your test or script.
        driver.get(url)
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
        funct.waitAndSend(driver, var.regV.phone, entry_info[7])
        funct.waitAndSend(driver, var.regV.ssn4, entry_info[8])
        funct.waitAndSend(driver, var.regV.dob, (entry_info[9] + entry_info[10] + entry_info[11]))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
        funct.waitAndSend(driver, var.regV.password, entry_info[12])
        funct.waitAndSend(driver, var.regV.passwordc, entry_info[12])
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)
# 2nd screen. OTP selection screen
        funct.waitAndClick(driver, var.otpV.text_button)
# 3rd screen. OTP code entry screen
        funct.waitAndSend(driver, var.otpV.otp_input, "111111")
        funct.waitAndClick(driver, var.otpV.otp_continue_button)
        time.sleep(5)
# 4th screen. Successful registration should redirect to Google.com.
# Checking that the search field on google.com is present on page.
        if driver.find_elements_by_name("q") != []:
             print("Initial registration successful.")
        else:
            driver.save_screenshot('test_screenshot_1.png')
            print("E---Redirect screen not reached on initial registration.")

    def test_reg2(self):
        driver = self.driver
# opens local file with user data
        notepadfile = open('/Users/nyl01072020.txt', 'r')
# variable for each line in the file
        entry_info = notepadfile.read().splitlines()
# The driver.get method will navigate to a page given by the URL.
# WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
# before returning control to your test or script.
        driver.get(url)
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
        funct.waitAndSend(driver, var.regV.phone, entry_info[7])
        funct.waitAndSend(driver, var.regV.ssn4, entry_info[8])
        funct.waitAndSend(driver, var.regV.dob, (entry_info[9] + entry_info[10] + entry_info[11]))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail2)
        funct.waitAndSend(driver, var.regV.password, entry_info[12])
        funct.waitAndSend(driver, var.regV.passwordc, entry_info[12])
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)
# Checking that error message appears and registration does not proceed.
        if driver.find_elements_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.button-wrap > p") != []:
             print("Error message received with duplicate email registration and failed as expected.")
        else:
            funct.fullshot(self)
            print("E---Error message did not appear or other unexpected behavior. Test Failed.")
        print("Test complete!")

# The tearDown method will get called after every test method. This is a place to do all cleanup actions.
    def tearDown(self):
        # NOTE: this code for checking for exceptions does NOT work for Safari
        # Python 3.8+ may have this built in. Need to revisit at future date.
        # checking for exceptions or assertion errors, if there are take screenshot
        for method, error in self._outcome.errors:
            if error:
                funct.fullshot(self)
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
# Boiler plate code to run the test suite
if __name__ == "__main__":
    unittest.main()