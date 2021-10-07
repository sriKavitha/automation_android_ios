# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, ElementNotVisibleException,ElementNotSelectableException,ElementNotInteractableException,NoSuchElementException
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

# [Documentation - Summary] Tests user workflow of failed
# registration with OTP pass and fake International passport on Browser method

# For use with Image file versions: Intlpassport.jpg, Intlpassportface.jpg

class NYlotto(confTest.NYlottoBASE):

    # This is the test case method. The test case method should always start with the characters test.
    # The first line inside this method creates a local reference to the driver object created in setUp method.
    def test_regIntlPassportBrowserFail(self):
        # Jira test ticket - https://rosedigital.atlassian.net/browse/NYL-2441
        testemail = self.testemail
        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")
        print("\nChecks failed registration with OTP pass and fake Driver's License on Browser method")
        print('\n----------\n' + 'Test setup')
        # Check for existing test user and wipe it from userpool prior to test execution
        try:
            funct.purgeSSOemail(self, testemail)
        except:
            pass
        print('----------')

        driver = self.driver
        # The driver.get method will navigate to a page given by the URL.
        # WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired)
        # before returning control to your test or script.
        # url is pulled from confTest
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
        funct.waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        # Clicks the checkbox for not supplying SSN4 info. Will send user thru ID Verification flow.
        funct.waitAndClick(driver, var.regV.ss_check)
        funct.waitAndSend(driver, var.regV.dob, (var.credsSSOWEB.dob_month + var.credsSSOWEB.dob_date + var.credsSSOWEB.dob_year))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
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
        funct.waitAndClick(driver, var.govIdV.passport_start_button)

        # alert for tester to interact with screen after
        try:
            driver.execute_script('alert("Test will pause for max of 5 minutes while tester uploads Intlpassport.jpg, Intlpassportface.jpg for gov id verification. '
                                  'STOP interacting with browser once last image is SAVED. '
                                  'This message will self-destruct in 5,4,3,2,1.");')
        except UnexpectedAlertPresentException:
            pass
        driver.switch_to.alert.text
        time.sleep(15)
        driver.switch_to.alert.accept()  # alert closed

        # wait for Submit button appears on summary screen
        ignore_list = [ElementNotVisibleException, ElementNotSelectableException, ElementNotInteractableException,
                       NoSuchElementException]
        wait = WebDriverWait(driver, timeout=300, poll_frequency=10, ignored_exceptions=ignore_list)
        wait.until(EC.element_to_be_clickable((By.XPATH, var.govIdV.id_submit_button[1])))

        # Submission screen - Automation will resume here, do NOT click the Submit button
        funct.waitAndClick(driver, var.govIdV.id_submit_button)
        time.sleep(15)
        # Last screen. Submission screen should show error message for an expected failure of identity verification.
        if "Sorry, we were unable to verify your information." in driver.page_source:
            print("PASS - ID Verification Failed message is expected and received!")
        # Successful registration would redirect to Google.com. Checking that the search field on google.com is present on page.
        elif driver.find_elements_by_name("q") != []:
            print("FAIL - Reached valid registration screen and redirected to callback uri.")
            funct.fullshot(driver)
            print('\n----------\n' + 'Test complete!\n\nTest clean up commencing')
            try:
                funct.purgeSSOemail(self, testemail)
            except:
                pass
            raise Exception('Unexpected behavior: please check screenshot')
        else:
            print("FAIL - Neither Identity verification error message reached nor Registration success screen reached (or text is incorrect/needs to be updated)")
            funct.fullshot(driver)
            print('\n----------\n' + 'Test complete!\n\nTest clean up commencing')
            try:
                funct.purgeSSOemail(self, testemail)
            except:
                pass
            raise Exception('Unexpected behavior: please check screenshot')

        # Deleting test data
        print('\n----------\n' + 'Test complete!\n\nTest clean up commencing')
        try:
            funct.purgeSSOemail(self, testemail)
        except:
            pass
        print('----------')


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if  confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))