# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest                   #Custom class for NYL
import HtmlTestRunner                               #Report runner

class NYlotto(confTest.NYlottoBASE):

# Checks First name change in update profile saves and redirects successfully
    def test_updateDOB(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        dobChange = '01011990'
        formattedChange = dobChange[:2] + "/" + dobChange[2:4] + "/" + dobChange[4:]
        print(formattedChange)
        funct.clearTextField(driver, var.updateProfV.dob)
        funct.waitAndSend(driver, var.updateProfV.dob, dobChange)
        funct.waitAndClick(driver, var.updateProfV.update_button)
        time.sleep(2)
        # 2nd screen. OTP selection screen
        funct.waitAndClick(driver, var.otpV.text_button)
        # 3rd screen. OTP code entry screen
        funct.waitAndSend(driver, var.otpV.otp_input, "111111")
        funct.waitAndClick(driver, var.otpV.otp_continue_button)
        time.sleep(5)
        # check for proper redirect to Google.com
        if driver.find_elements_by_name("q") != []:
            print('Update profile successfully redirected to Google.')
        else:
            funct.fullshot(driver)
            print('FAIL - Update profile redirect screen not reached. Test can not proceed.')
            try:
                funct.purge(self, testemail)
                print('test user purged')
            except:
                print('no test user found')
            print("Test complete!")
            raise Exception('Update profile redirected incorrectly')
        # Checks the change has been saved to the profile
        driver.get(self.update_url)
        time.sleep(5)
        change = driver.find_element(var.updateProfV.dob[0], var.updateProfV.dob[1])
        if funct.checkValue(driver, var.updateProfV.dob, formattedChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.dob[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.dob, formattedChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.dob[2] + ' field should say "' + dobChange + '" , but says "' + change.get_attribute(
                    "value") + '"!')
            funct.fullshot(driver)
            try:
                funct.purge(self, testemail)
                print('test user purged')
            except:
                print('no test user found')
            print("Test complete!")
            raise Exception('Update profile changes failed to save.')

        # Deleting test data
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')
        print("Test complete!")


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))