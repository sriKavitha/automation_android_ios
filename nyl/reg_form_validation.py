# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"
url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"

class NYlotto(confTest.NYlottoBASE):

# Checks main error appears when empty form is submitted
    def test01_regSubmitError(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndClick(driver, var.regV.submit_button)
        if funct.checkError(driver, var.regV.submit_button_error) == True:
            print("PASS - " + var.regV.submit_button_error[2] + " is present.")
        elif funct.checkError(driver, var.regV.submit_button_error) == False:
            print("FAIL - " + var.regV.submit_button_error[2] + " is missing")
            funct.fullshot(driver)
            raise Exception('Error warning element not found.')

# Checks main error copy
    def test02_regSubmitErrorCopy(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndClick(driver, var.regV.submit_button)
        warning = driver.find_element(var.regV.submit_button_error[0], var.regV.submit_button_error[1])
        if funct.checkErrorText(driver, var.regV.submit_button_error, var.regV.submitErrorStub) == True:
            print("PASS - Warning copy text is correct.")
        elif funct.checkErrorText(driver, var.regV.submit_button_error, var.regV.submitErrorStub) == False:
            print("FAIL - Warning should say " + var.regV.submitErrorStub + " , but says " + warning.get_attribute("innerText") + "!")
            funct.fullshot(driver)
            raise Exception('Error copy is incorrect.')

# Checks mandatory field errors are found
    def test03_regRequiredErrors(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndClick(driver, var.regV.submit_button)
        warningList = []
        # These are the CSS selectors for the 12 red text error elements
        warningsExpected = [
             var.regV.fname_error, var.regV.lname_error, var.regV.housenum_error,
             var.regV.street_error, var.regV.city_error, var.regV.state_dropdown_error,
             var.regV.zip_error, var.regV.phone_error, var.regV.dob_error,
             var.regV.email_error, var.regV.password_error, var.regV.confirmPsw_error]
        for warning in warningsExpected:
            if funct.checkError(driver, warning) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print("PASS - Error warnings found and present.")
        elif len(warningList) > 0:
            print("FAIL - ")
            print(warningList)
            print("Error warning(s) missing")
            funct.fullshot(driver)
            raise Exception("Error warning element not found.")

# Checks mandatory field error copy
    def test04_regRequiredErrorsCopy(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndClick(driver, var.regV.submit_button)
        warningList = []
        # These are the CSS selectors for the 12 red text error elements
        warningsExpected = [
             var.regV.fname_error, var.regV.lname_error, var.regV.housenum_error,
             var.regV.street_error, var.regV.city_error, var.regV.state_dropdown_error,
             var.regV.zip_error, var.regV.phone_error, var.regV.dob_error,
             var.regV.email_error, var.regV.password_error, var.regV.confirmPsw_error]
        for warning in warningsExpected:
            if funct.checkErrorText(driver, warning, var.regV.requiredErrorStub) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print("PASS - Error warnings found and copy is correct.")
        elif len(warningList) > 0:
            print("FAIL - ")
            print(warningList)
            print("Error warning(s) copy is incorrect.")
            funct.fullshot(driver)
            raise Exception("Error warning(s) copy is incorrect.")

# Checks that certain fields do not take letters
    def test05_regUnacceptedLetterErrors(self):
        driver = self.driver
        driver.get(url)
        # grabbing every text field and inputting letters into it, triggering error
        textFields = driver.find_elements_by_class_name("form-control")
        valueInputted = "asd"
        valueExpected = ""
        for field in textFields:
            field.send_keys(valueInputted)
        warningList = []
        # These are the fields that do not take letters and will have error elements
        warningsExpected = [
            var.regV.zip, var.regV.phone, var.regV.ssn4, var.regV.dob]
        for warning in warningsExpected:
            if funct.checkValue(driver, warning, valueExpected) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print("PASS - invalid values '" + valueInputted + "' not accepted in appropriate fields")
        elif len(warningList) > 0:
            print("FAIL - invalid values '" + valueInputted + "' are allowed in")
            print(warningList)
            print(" fields.")
            funct.fullshot(driver)
            raise Exception("Invalid values allowed in fields.")

# Checks that certain fields do not take symbols
    def test06_regUnacceptedSymbolsErrors(self):
        driver = self.driver
        driver.get(url)
        # grabbing every text field and inputting symbols into it, triggering error
        textFields = driver.find_elements_by_class_name("form-control")
        valueInputted = "!@#"
        valueExpected = ""
        for field in textFields:
            field.send_keys(Keys.SHIFT + "1" + "2" + "3")
        warningList = []
        # These are the fields that do not take letters and will have error elements
        warningsExpected = [
            var.regV.fname, var.regV.mname, var.regV.lname,
            var.regV.zip, var.regV.phone, var.regV.ssn4, var.regV.dob]
        for warning in warningsExpected:
            if funct.checkValue(driver, warning, valueExpected) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print("PASS - invalid values '" + valueInputted + "' not accepted in appropriate fields")
        elif len(warningList) > 0:
            print("FAIL - invalid values '" + valueInputted + "' are allowed in")
            print(warningList)
            print(" fields.")
            funct.fullshot(driver)
            raise Exception("Invalid values allowed in fields.")

# Checks that certain fields do not take numbers
    def test07_regUnacceptedNumbersErrors(self):
        driver = self.driver
        driver.get(url)
        # grabbing every text field and inputting numbers into it, triggering error
        textFields = driver.find_elements_by_class_name("form-control")
        valueInputted = "123"
        valueExpected = ""
        for field in textFields:
            field.send_keys("123")
        warningList = []
        # These are the fields that do not take letters and will have error elements
        warningsExpected = [
            var.regV.fname, var.regV.mname, var.regV.lname]
        for warning in warningsExpected:
            if funct.checkValue(driver, warning, valueExpected) == False:
                warningList.append(warning[2])
        if len(warningList) <= 0:
            print("PASS - invalid values '" + valueInputted + "' not accepted in appropriate fields")
        elif len(warningList) > 0:
            print("FAIL - invalid values '" + valueInputted + "' are allowed in")
            print(warningList)
            print(" fields.")
            funct.fullshot(driver)
            raise Exception("Invalid values allowed in fields.")

# Checks for appearance of error messages when inputting invalid data in zip code field
    def test08_regInvalidFormatZipcode(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.zip, "123")
        funct.waitAndSend(driver, var.regV.zip, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.zip_error, var.regV.zipErrorStub) == True:
            print("PASS - " + var.regV.zip_error[2] + " is present and copy correctly reads as '" + var.regV.zipErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.zip_error, var.regV.zipErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.zipErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting invalid data in phone field
    def test09_regInvalidFormatPhone(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.phone, "123")
        funct.waitAndSend(driver, var.regV.phone, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.phone_error, var.regV.phoneErrorStub) == True:
            print("PASS - " + var.regV.phone_error[2] + " is present and copy correctly reads as '" + var.regV.phoneErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.phone, var.regV.phoneErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.phoneErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting invalid data in DOB field
    def test10_regInvalidFormatDOB(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.dob, "123")
        funct.waitAndSend(driver, var.regV.dob, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.dob_error, var.regV.dobErrorStub) == True:
            print("PASS - " + var.regV.dob_error[2] + " is present and copy correctly reads as '" + var.regV.dobErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.dob_error, var.regV.dobErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.dobErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting invalid data in email field
    def test11_regInvalidFormatEmail(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.email, "123")
        funct.waitAndSend(driver, var.regV.email, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.email_error, var.regV.emailErrorStub) == True:
            print("PASS - " + var.regV.email_error[2] + " is present and copy correctly reads as '" + var.regV.emailErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.email_error, var.regV.emailErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.emailErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting only numbers in password field
    def test12_regInvalidFormatPswNumbers(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.password, "123456789")
        funct.waitAndSend(driver, var.regV.password, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == True:
            print("PASS - " + var.regV.password_error[2] + " is present and copy correctly reads as '" + var.regV.passwordErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.passwordErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting only letters in password field
    def test_13regInvalidFormatPswLetters(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.password, "asdftest")
        funct.waitAndSend(driver, var.regV.password, Keys.TAB)
        if funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == True:
            print("PASS - " + var.regV.password_error[2] + " is present and copy correctly reads as '" + var.regV.passwordErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.passwordErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting special characters in password field
    def test_14regInvalidFormatPswSymbols(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.password, "test")
        funct.waitAndSend(driver, var.regV.password, Keys.SHIFT + "1")
        funct.waitAndSend(driver, var.regV.password, "test")
        funct.waitAndSend(driver, var.regV.password, Keys.TAB)
        print(driver.find_element(var.regV.password[0],var.regV.password[1]).get_attribute("value"))
        if funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == True:
            print("PASS - " + var.regV.password_error[2] + " is present and copy correctly reads as '" + var.regV.passwordErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.password_error, var.regV.passwordErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.passwordErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when inputting mismatched passwords
    def test_15regMismatchedPsw(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.password, "test")
        funct.waitAndSend(driver, var.regV.confirmPsw, Keys.SHIFT + "1")
        funct.waitAndSend(driver, var.regV.confirmPsw, Keys.TAB)
        # checking updated error message text
        if funct.checkErrorText(driver, var.regV.confirmPsw_error, var.regV.confirmPswErrorStub) == True:
            print("PASS - " + var.regV.confirmPsw_error[2] + " is present and copy correctly reads as '" + var.regV.confirmPswErrorStub + "'")
        elif funct.checkErrorText(driver, var.regV.confirmPsw_error, var.regV.confirmPswErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.confirmPswErrorStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when underage Date of Birth is inputted
    def test_16regUnderage(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndSend(driver, var.regV.dob, "01/01/2018")
        funct.waitAndSend(driver, var.regV.dob, Keys.TAB)
        # checking updated error message text
        if funct.checkErrorText(driver, var.regV.dob_error, var.regV.dobErrorUnderageStub) == True:
            print("PASS - " + var.regV.dob_error[2] + " is present and copy correctly reads as '" + var.regV.dobErrorUnderageStub + "'")
        elif funct.checkErrorText(driver, var.regV.dob_error, var.regV.dobErrorStub) == False:
            print("FAIL - Error warning copy is incorrect and does not read '" + var.regV.dobErrorUnderageStub + "'")
            funct.fullshot(driver)
            raise Exception('Error warning copy is incorrect.')

# Checks for appearance of error messages when mandatory checkboxes are not checked
    def test_17regChkbxErrors(self):
        driver = self.driver
        driver.get(url)
        # triggering error
        funct.waitAndClick(driver, var.regV.submit_button)
        # checking for error messages
        formChecks = driver.find_elements_by_class_name("form-check-label")
        # print(len(formChecks))
        checkCounter = 0
        checkCounterExpected = 2
        for elem in formChecks:
            if "form-check-label error" in elem.get_attribute("class"):
                checkCounter = checkCounter+1
        if checkCounter == checkCounterExpected:
            print("PASS - All checkbox text color change errors are present.")
        else:
            print("FAIL - expected " + str(checkCounterExpected) + " red text changes, but found " + str(checkCounter) + ".")
            funct.fullshot(driver)
            raise Exception('Error warning(s) missing.')

# Boiler plate code to run the test suite
if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))