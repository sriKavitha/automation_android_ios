from selenium import webdriver
import warnings
import unittest, time, re
from selenium.webdriver.common.keys import Keys

#Successful registration with valid SSN4
#url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
#url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&redirectUri=https://google.com"
testemail = "marie.liao+ssotest@rosedigital.co"

class NYlotto(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.driver = webdriver.Remote(
           command_executor='http://192.168.86.26:4444/wd/hub',
           desired_capabilities= {
               "browserName": "chrome",
               "version": "",
               "platform": "ANY",
               "javascriptEnabled": True,
               'chromeOptions': {
                   'useAutomationExtension': False,
                   'args': ['--disable-infobars']
               }
          })
        #self.driver = webdriver.Chrome()

        # self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(12)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_reg(self):
        driver = self.driver
        # notepadfile = open('/Users/nyl.txt', 'r')     #soft fail with SSN4 check, sends to GovID verification
        notepadfile = open('/Users/nylUser.txt', 'r')  #successful registration with SSN4
        entry_info = notepadfile.readlines()
        driver.get(url)

#naming the elements right off the bat, for ease
        fname = driver.find_element_by_name("firstName")
        lname = driver.find_element_by_name("lastName")
        housenum = driver.find_element_by_name("streetNumber")
        street = driver.find_element_by_name("street")
        #add2 = driver.find_element_by_name("addressLine2")
        city = driver.find_element_by_name("city")
        state_dropdown = driver.find_element_by_name("state")
        #state_ny = driver.find_element_by_css_selector("#address_state > option:nth-child(34)")
        zip = driver.find_element_by_name("zip")
        phone = driver.find_element_by_name("phone")
        ssn4 = driver.find_element_by_name("ssn4")
        #ss_check = driver.find_element_by_name("noSsn4")
        dob_month = driver.find_element_by_name("birthdate")
        dob_check = driver.find_element_by_name("isOver18")
        email = driver.find_element_by_id("sso-email")
        password = driver.find_element_by_name("password")
        passwordc = driver.find_element_by_name("confirmPassword")
        tos_check = driver.find_element_by_name("acceptedTermsAndConditions")
        #promo_check = driver.find_element_by_id("entitlements_promo_emails")
        submit_button = driver.find_element_by_class_name("nyl-btn")


#telling them what to do via the info on the .txt doc
        fname.send_keys(entry_info[0])
        lname.send_keys(entry_info[1])
        housenum.send_keys(entry_info[2])
        street.send_keys(entry_info[3])
        city.send_keys(entry_info[4])
        state_dropdown.click()
#This is a fun one, I'm basically telling the dropdown to keep scrolling down until it sees the choice (NY) that we want
        #by using driver.find_elements_by_css_selector (PLURAL) on the css selector of the NY option, it returns either
        #an empty list "[]" if it can't find any instances of that selector, OR it returns a list of the instances it can find
        # so, the script is saying "While you are returning an empty list, press down. once the list is NOT empty, click NY"
        counter = 0
        while counter != 1:
            check = driver.find_elements_by_css_selector("#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > select > option:nth-child(38)")
            if check == []:
                state_dropdown.send_keys(Keys.DOWN)
            else:
                print("yay")
                counter = 1
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