# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys  # Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By  # By class provides method for finding the page elements by NAME, ID, XPATH, etc.
import var, funct, util, confTest, HtmlTestRunner  # Custom class for NYL


# [Documentation - Summary] Tests user workflow of failed
# registration with OTP pass and fake US passport on Browser method
# For use with Entry Info file version: nyl04082020.txt
# For use with Image file versions: DLback.jpg, DLface.jpg, DLfront.jpg
# USpassport.jpg, USface.jpg, Intlpassport.jpg, Intlpassportface.jpg
# Change paths starting on Line 104 for reading images prior to running test

class NYlotto(confTest.NYlottoBASE):

    # This is the test case method. The test case method should always start with the characters test.
    # The first line inside this method creates a local reference to the driver object created in setUp method.
    def test_regUSPassportBrowserFail(self):
        # Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-2440
        # Check for existing test user and wipe it from userpool prior to test execution
        try:
            funct.purge(self, self.testemail)
            print('test user purged')
        except:
            print('no test user found')
        driver = self.driver
        # The driver.get method will navigate to a page given by the URL.
        # WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
        # before returning control to your test or script.
        # url is pulled from confTest
        driver.get(self.url)
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
        funct.waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        # Clicks the checkbox for not supplying SSN4 info. Will send user thru ID Verification flow.
        funct.waitAndClick(driver, var.regV.ss_check)
        funct.waitAndSend(driver, var.regV.dob,
                          (var.credsSSOWEB.dob_month + var.credsSSOWEB.dob_date + var.credsSSOWEB.dob_year))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, self.testemail)
        funct.waitAndSend(driver, var.regV.password, var.credsSSOWEB.password)
        funct.waitAndSend(driver, var.regV.confirmPsw, var.credsSSOWEB.password)
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
        #        USpassport.jpg, USface.jpg
        funct.waitAndClick(driver, var.govIdV.passport_start_button)
        # 6th screen. Upload Front of Passport
        funct.waitAndSend(driver, var.govIdV.passport_capture_button, "/Users/Shared/testing/USpassport.jpg")
        # 7th screen. Quality check & Save
        funct.waitAndClick(driver, var.govIdV.passport_save_button)
        # 8th screen. Upload Facial Snapshot
        funct.waitAndSend(driver, var.govIdV.passport_facial_capture_button, "/Users/Shared/testing/USface.jpg")
        # 9th screen. Quality check & Save
        time.sleep(2)
        funct.waitAndClick(driver, var.govIdV.passport_facial_save_button)
        # 10th screen. Submit all docs for id verification
        funct.waitAndClick(driver, var.govIdV.passport_submit_button)
        # Last screen. Screen should show error message for identity verification.
        # Successful registration would redirect to Google.com. Checking that the search field on google.com is present on page.
        if "Sorry, we were unable to verify your information." in driver.page_source:
            print("PASS - ID Verification Failed message is expected and received!")
        elif driver.find_elements_by_name("q") != []:
            print("FAIL - Reached valid registration screen and redirected to callback uri.")
            funct.fullshot(driver)
            try:
                funct.purge(self, self.testemail)
                print('test user purged')
            except:
                print('no test user found')
            raise Exception('Registration redirected incorrectly.')
        else:
            print(
                "FAIL - Neither Identity verification error message reached nor Registration success screen reached (or text is incorrect/needs to be updated)")
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
            print('test user purged')
        except:
            print('no test user found')
        print("Test complete!")


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if  confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))