# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver
import warnings
import unittest, time, re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import var
import funct

# [Documentation - Summary] Tests user workflow of successful
# registration with valid SSN4 and OTP pass

# [Documentation - Variables] Test file specific variables
url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"
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

        # self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(12)
        self.verificationErrors = []
        self.accept_next_alert = True

#Test case
    def test_reg(self):
        driver = self.driver
        notepadfile = open('/Users/nylUser.txt', 'r')  #local file with user data
        entry_info = notepadfile.readlines()
        driver.get(url)

#Instructions for webdriver to read and input user data via the info on the .txt doc
        # funct.waitAndSend(var.regV.fname, entry_info[0])
        time.sleep(3)
        print(var.regV.fname)
        funct.waitAndSend(driver, var.regV.fname, entry_info[0])
        funct.waitAndSend(driver, var.regV.lname, entry_info[1])
        funct.waitAndSend(driver, var.regV.housenum, entry_info[2])
        funct.waitAndSend(driver, var.regV.city, entry_info[4])

#Find and select the state according to the info in the .txt doc
        funct.waitAndClick(driver, var.regV.state_dropdown)
        driver.find_element_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > select > option:nth-child(38)").click()

        zip.send_keys(entry_info[5])
        phone.send_keys(entry_info[6])
        ssn4.send_keys(entry_info[7])
        #ss_check.click()   #not clicked for successful registration with SSN4
        dob_month.send_keys(entry_info[8] + entry_info[9] + entry_info[10])
        #dob_day.send_keys(entry_info[9])
        #dob_year.send_keys(entry_info[10])
        dob_check.click()
        email.send_keys(testemail)
        password.send_keys(entry_info[11])
        passwordc.send_keys(entry_info[11])
        tos_check.click()
        submit_button.click()
#implicit wait for #2nd screen to load elements
        # driver.implicitly_wait(10)
        # otp_header = driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > h3.confirm-otp-header')
        time.sleep(10)
#2nd screen. OTP selection screen
        driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > div > button.nyl-btn-single.button-1').click()
        driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div/div[1]/div/input").send_keys("111111")
        driver.find_element_by_css_selector('#app-container > div > div.container__content > div > div > form > div > div:nth-child(4) > button > span').click()
        time.sleep(10)
#3rd screen. Successful registration should redirect to Google.com. Checking that the search field on google.com is present on page.
        if driver.find_elements_by_name("q") != []:
             print("registration successful and redirected to callback uri")
        else:
            driver.save_screenshot('test_screenshot_1.png')
            print("E---Redirect screen not reached")
        print("Test complete!")

    def tearDown(self):
       # self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()