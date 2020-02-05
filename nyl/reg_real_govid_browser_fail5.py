# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
import var, funct, util                             #Custom class for NYL

# [Documentation - Summary] Tests user workflow of failed
# registration with OTP pass and random images with Passport upload on Browser method
# For use with Entry Info file version: nyl01072020.txt
# For use with Image file versions: Random-landscape.jpg, Random-portrait.jpg
# Change paths starting on Line 104 for reading images prior to running test

# [Documentation - Variables] Test file specific var
#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"
url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
testemail = "marie.liao+ssotest@rosedigital.co"

class NYlotto(unittest.TestCase):

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
    def test_regpassport(self):
        driver = self.driver
        # opens local file with user data
        notepadfile = open('/Users/nyl01072020.txt', 'r')
        # variable for each line in the file
        entry_info = notepadfile.read().splitlines()
        # The driver.get method will navigate to a page given by the URL.
        # WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
        # before returning control to your test or script.
        driver.get(url)
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
        # Clicks the checkbox for not supplying SSN4 info. Will send user thru ID Verification flow.
        funct.waitAndClick(driver, var.regV.ss_check)
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
# 4th screen. Gov ID document capture selection screen
# Choosing Passport and Continue on Browser
        funct.waitAndClick(driver, var.govIdV.gov_id_dropdown)
        funct.waitAndClick(driver, var.govIdV.id_passport)
        funct.waitAndClick(driver, var.govIdV.gov_id_dropdown)
        funct.waitAndClick(driver, var.govIdV.browser_link)
        time.sleep(5)
# 5th screen. Initiate document capture process
# uploading the different images for the gov id verification
# Random-landscape.jpg, Random-portrait.jpg
        funct.waitAndClick(driver, var.govIdV.passport_start_button)
# 6th screen. Upload Front of Passport
        funct.waitAndSend(driver, var.govIdV.passport_capture_button, "/Users/marieliao/Desktop/Random-landscape.jpg")
# 7th screen. Quality check & Save
        funct.waitAndClick(driver, var.govIdV.passport_save_button)
# 8th screen. Upload Facial Snapshot
        funct.waitAndSend(driver, var.govIdV.passport_facial_capture_button, "/Users/marieliao/Desktop/Random-portrait.jpg")
# 9th screen. Quality check & Save
        time.sleep(2)
        funct.waitAndClick(driver, var.govIdV.passport_facial_save_button)
# 10th screen. Submit all docs for id verification
        funct.waitAndClick(driver, var.govIdV.passport_submit_button)
# Last screen. Screen should show error message for identity verification.
# Successful registration would redirect to Google.com. Checking that the search field on google.com is present on page.
        if "Sorry, we were unable to verify your information." in driver.page_source:
             print("ID Verification Failed message is expected and received!")
        elif driver.find_elements_by_name("q") != []:
            print("E----Reached valid registration screen and redirected to callback uri.")
            funct.fullshot(self)
        else:
            funct.fullshot(self)
            print("E---Neither Identity verification error message reached nor Registration success screen reached (or text is incorrect/needs to be updated)")
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