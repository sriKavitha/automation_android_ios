from selenium import webdriver
import warnings
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import sys


url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
#url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"

class NYlotto(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        # self.driver = webdriver.Remote(
        #     command_executor='http://192.168.86.26:4444/wd/hub',
        #     desired_capabilities={
        #         "browserName": "chrome",
        #         "version": "",
        #         "platform": "ANY",
        #         "javascriptEnabled": True,
        #         'chromeOptions': {
        #             'useAutomationExtension': False,
        #             'args': ['--disable-infobars']
        #         }
        #     })
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(12)
        self.verificationErrors = []
        self.accept_next_alert = True



    def test_reg(self):
        driver = self.driver
        driver.get(url)
#check red text errors
        driver.find_element_by_class_name("nyl-btn").click()
        if driver.find_element_by_class_name("submit-error").text != "Please see required fields above to complete registration.":
            print("Main error is incorrect or missing")
#these are the CSS selectors for the 12 red text error elements
        warningsExpected = [
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(2) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(4) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(6) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(7) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(9) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > div",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(11) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.has-prepend > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(15) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.form-group.has-prepend > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(3) > div.is-error.invalid-feedback",
            "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(4) > div.is-error.invalid-feedback"]
#This grabs every element that has the class name "is-error" (should be the same 12 elements from the list above)
        warningsActual = driver.find_elements_by_class_name("is-error")
#These are the labels for the 12 red text error elements (null is put first, because counting in python starts at zero)
        warningLabels = ["null", "First Name", "Last Name", "House #", "Street Name", "City/town", "State", "Zipcode", "Phone#", "date of Birth", "Email", "Original Password", "Confirm Password"]
#This is a counter, you will see it in work shortly
        counter = 0
#checks if the length of the list generated automatically (warningsActual) is the same length as the hardcoded list we have (warningsExpected)
        if len(warningsExpected) == len(warningsActual):
            print ("All warning texts found!")
#If these are NOT the same length, it will send an error and go down the list, checking which one is missing and report it
        else:
            print("E---Expected " + str(len(warningsExpected)) + " warnings but found " + str(len(warningsActual)) + " warnings!")
        for warning in warningsExpected:
    #counter counts up, allowing us to pick the right label
            counter = counter+1
            try:
                driver.find_element_by_css_selector(warning)
            except:
                print(warningLabels)
                print("E---" + warningLabels[counter] + " warning Not Found!")
                print(warning)
#resetting counter
        counter = 0
        for warning in warningsActual:
            counter = counter + 1
#checking the text of the warning
            if warning.text != "Required":
                print("E---" + warningLabels[counter] + " warning should say 'required', but says " + warning.text + "!")
#grabbing every text field and writing the word "test" into it... where allowed
        textFields = driver.find_elements_by_class_name("form-control")
        for field in textFields:
            field.send_keys("test")
        if driver.find_element_by_name("zip").get_attribute("value") != "":
            print("E---alphabet letters allowed in zipcode field!")

    #checking which of the forms still have warnings in them
        warningsActual2 = driver.find_elements_by_class_name("is-error")
        if len(warningsActual2) != 6:
            print("E---Expected 6 warning texts, instead found " + str(len(warningsActual2)))
#check remaining text by individual css selectors
        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > div").text != "Required":
            print("E--- State warning message is incorrect, should be 'required', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > div").text)


        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(11) > div.is-error.invalid-feedback").text != "Required":
            print("E--- Zip Code warning message is incorrect, should be 'required', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(11) > div.is-error.invalid-feedback").text)

        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.form-group.has-prepend > div.is-error.invalid-feedback").text != "Invalid email address":
            print("E--- Original Email warning message is incorrect, should be 'Invalid email address', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.form-group.has-prepend > div.is-error.invalid-feedback").text)

        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.has-prepend > div.is-error.invalid-feedback").text != "Required":
            print("E--- Phone# warning message is incorrect, should be 'required', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.has-prepend > div.is-error.invalid-feedback").text)

        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(15) > div.is-error.invalid-feedback").text != "Required":
            print("E--- DoB warning message is incorrect, should be 'required', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(15) > div.is-error.invalid-feedback").text)

        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(3) > div.is-error.invalid-feedback").text != "Your password must follow the password guidelines.":
            print("E--- DoB warning message is incorrect, should be 'Your password must follow the password guidelines.', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(3) > div.is-error.invalid-feedback").text)

#trigger mismatching passwords and check updated error message text
        driver.find_element_by_name("confirmPassword").send_keys("testtest")
        if driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(4) > div.is-error.invalid-feedback").text != "Passwords must match":
            print("E--- DoB warning message is incorrect, should be 'Passwords must match', but instead says " + driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(4) > div.is-error.invalid-feedback").text)

#Check checkbox forms
        formChecks = driver.find_elements_by_class_name("form-check-label")
        #print(len(formChecks))
        checkCounter = 0
        checkCounterExpected = 2
        for elem in formChecks:
            if "error" in elem.get_attribute("class"):
                checkCounter = checkCounter+1
        if checkCounter == checkCounterExpected:
            print ("All text color change errors are correct!")
        else:
            print ("E---expected " + str(checkCounterExpected) + " red text changes, but found " + str(checkCounter) + "!")
        checkBoxes = driver.find_elements_by_class_name("form-check-input")
        for checkBox in checkBoxes:
                checkBox.click()
        driver.find_element_by_class_name("nyl-btn").click()
# input numbers into number fields, check secondary error results
        driver.find_element_by_name("zip").send_keys("1")
        driver.find_element_by_name("phone").send_keys("1")
        driver.find_element_by_name("birthdate").send_keys("1")
        if "Invalid zipcode" not in driver.page_source:
            print("E---'Invalid Zipcode' warning not found!")
        if "Invalid phone number" not in driver.page_source:
            print("E---'Invalid phone number' warning not found!")
        if "Please enter a valid birth date" not in driver.page_source:
            print("E---'Please enter a valid birth date' warning not found!")
        driver.find_element_by_name("birthdate").send_keys("0102010")
        if "You must be 18 years or older to register" not in driver.page_source:
            print("E---'You must be 18 years or older to register' warning not found!")
#putting in acceptable but invalid data
        driver.find_element_by_name("state").click()
        driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(10) > div > select > option:nth-child(2)").click()
        driver.find_element_by_name("zip").send_keys("1001")
        driver.find_element_by_name("phone").clear()
        driver.find_element_by_name("phone").send_keys("5558675309")
        driver.find_element_by_name("birthdate").clear()
        driver.find_element_by_name("birthdate").send_keys("10311910")
        driver.find_element_by_id("sso-email").send_keys("qa@qa.co")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("Test1234")
        driver.find_element_by_name("confirmPassword").clear()
        driver.find_element_by_name("confirmPassword").send_keys("Test1234")
        if driver.find_element_by_class_name("submit-error").text != "Please see required fields above to complete registration.":
            print("Main error is incorrect or missing")
        time.sleep(1)
        driver.find_element_by_class_name("nyl-btn").click()
        time.sleep(5)

#checking that we get to the "can not verify" screen
        try:
            driver.find_elements_by_class_name("migration-failed-body")
        except:
            print("Can not find Identity verification failed screen")

        if "Sorry, we cannot verify your identity." in driver.page_source:
             print("Identity verification failed screen reached!")
        elif driver.find_elements_by_name("q") != []:
            print("E----Reached valid screen and redirected to callback uri")
            driver.save_screenshot('test_screenshot_1.png')
        else:
            driver.save_screenshot('test_screenshot_2.png')
            print("E---Neither Identity verification failed nor valid screen reached (or text is incorrect/needs to be updated)")
        print("Test complete!")
    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()