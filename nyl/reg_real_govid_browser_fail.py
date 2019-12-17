# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
import var                                          #Custom class for NYL
import funct                                        #Custom class for NYL

# [Documentation - Summary] Tests user workflow of failed
# registration with OTP pass and fake Government ID on Browser method
# For use with Entry Info file version: nyl12122019.txt
# For use with Image file versions: DLback.jpg, DLface.jpg, DLfront.jpg
# USpassport.jpg, USface.jpg, Intlpassport.jpg, Intlpassportface.jpg

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
    def test_reg(self):
        driver = self.driver
        # opens local file with user data
        notepadfile = open('/Users/nyl12122019.txt', 'r')
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
        # Clicks the checkbox for not supplying SSN4 info. Will send user thru ID Verification flow.
        funct.waitAndClick(driver, var.regV.ss_check)
        funct.waitAndSend(driver, var.regV.dob, (entry_info[9] + entry_info[10] + entry_info[11]))
        funct.waitAndClick(driver, var.regV.dob_check)
        funct.waitAndSend(driver, var.regV.email, testemail)
        funct.waitAndSend(driver, var.regV.password, entry_info[12])
        funct.waitAndSend(driver, var.regV.passwordc, entry_info[12])
        funct.waitAndClick(driver, var.regV.tos_check)
        funct.waitAndClick(driver, var.regV.submit_button)

#implicit wait for #2nd screen to load elements
        # driver.implicitly_wait(10)
        # otp_header = driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > h3.confirm-otp-header')
        time.sleep(10)
#2nd step. OTP selection screen
        driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > div > button.nyl-btn-single.button-1').click()
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div/div[1]/div/input").send_keys("111111")
        driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > form > div > div:nth-child(4) > button > span').click()
        time.sleep(10)
#3rd step. Gov ID selection screen
        # counter = 0
        # while counter != 1:
        #     check = driver.find_elements_by_css_selector("#app-container > div > div.container__content > div > div > form > div > div.form-group > div > select > option:nth-child(2)")
        #     if check == []:
        #         govid_dropdown = driver.find_element_by_name("govIdType")
        #         govid_dropdown.send_keys(Keys.DOWN)
        #     else:
        #         print("selected id type")
        #         counter = 1
        govid_dropdown = driver.find_element_by_name("govIdType")
        govid_dropdown.send_keys(Keys.DOWN)
        govid_dropdown.send_keys(Keys.ENTER)
        driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div > div.form-group > div > select > option:nth-child(2)").click()
        driver.find_element_by_class_name("continue-with-browser-link").click()
        time.sleep(5)
#uploading the different images for the gov id verification
        driver.find_element_by_id("dcui-start-button").click()
        chooseFile1 = driver.find_element_by_id("capture-input")
        chooseFile1.send_keys("/Users/foley/Downloads/dlfront.jpg")
        driver.find_element_by_id("save-capture").click()
        chooseFile2 = driver.find_element_by_id("capture-input")
        chooseFile2.send_keys("/Users/foley/Downloads/dlback.jpg")
        driver.find_element_by_id("save-capture").click()
        # waitAndClick("by.ID", "save-capture").click()
        chooseFile3 = driver.find_element_by_id("capture-input")
        chooseFile3.send_keys("/Users/foley/Downloads/dlface.jpg")
        driver.find_element_by_css_selector("#save-capture").click()
        # waitAndClick("by.ID", "verify-all")
        time.sleep(10)
        driver.find_element_by_id("verify-all").click()
        time.sleep(5)
#last screen. Screens should show error message for identity verification. Successful registration would redirect to Google.com. Checking that the search field on google.com is present on page.
        if "Sorry, we were unable to verify your information." in driver.page_source:
             print("Error message received!")
        elif driver.find_elements_by_name("q") != []:
            print("E----Reached valid screen and redirected to callback uri")
            driver.save_screenshot('test_screenshot_1.png')
        else:
            driver.save_screenshot('test_screenshot_2.png')
            print("E---Neither Identity verification error message reached nor Registration success screen reached (or text is incorrect/needs to be updated)")
        print("Test complete!")

    def tearDown(self):
       # self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()