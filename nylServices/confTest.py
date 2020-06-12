# [Documentation - Setup] This section lists all dependencies
# that are imported for this test file to work
from selenium import webdriver  #webdriver module provides all WebDriver implementations
import warnings
from browsermobproxy import Server
import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys     #Keys class provide keys in the keyboard like RETURN, F1, ALT, etc.
from selenium.webdriver.common.by import By         #By class provides method for finding the page elements by NAME, ID, XPATH, etc.
from selenium.webdriver.support.ui import Select    #Select class provides ability to select items in dropdown
import var, funct                  #Custom class for NYL

class NYLservicesBASE(unittest.TestCase):
# report can be "html" for testrunner reports or "terminal" for direct terminal feedback
    report = 'terminal'
    #report = "html"

    # The setUp is part of initialization, this method will get called before every test function which you
    # are going to write in this test case class.

    def setUp(self):
        # .env can be "dev", "qa", or "stage" to denote which environment and credentials to use
        self.env = 'dev'

        self.testemail = "marie.liao+ssotest@rosedigital.co"

        # if self.env == 'dev':
        #     self.url = "https://sso-dev.nylservices.net/?clientId=29d5np06tgg87unmhfoa3pkma7&callbackUri=https://google.com"
        #     self.login_url = "https://sso-dev.nylservices.net/login?clientId=29d5np06tgg87unmhfoa3pkma7&callbackUri=https://google.com"
        #     self.reset_url = "https://sso-dev.nylservices.net/reset-password?clientId=29d5np06tgg87unmhfoa3pkma7"
        #     self.update_url = "https://sso-dev.nylservices.net/update-profile?clientId=29d5np06tgg87unmhfoa3pkma7&callbackUri=https://google.com"
        # elif self.env == 'qa':
        #     self.url = "https://sso-qa.nylservices.net/?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
        #     self.login_url = "https://sso-qa.nylservices.net/login?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
        #     self.reset_url = "https://sso-qa.nylservices.net/reset-password?clientId=4a0p01j46oms3j18l90lbtma0o"
        #     self.update_url = "https://sso-qa.nylservices.net/update-profile?clientId=4a0p01j46oms3j18l90lbtma0o&callbackUri=https://google.com"
        # elif self.env == 'stage':
        #     self.url = "https://sso-stage.nylservices.net/?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
        #     self.login_url = "https://sso-stage.nylservices.net/login?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"
        #     self.reset_url = "https://sso-stage.nylservices.net/reset-password?clientId=6pdeoajlh4ttgktolu3jir8gp6"
        #     self.update_url = "https://sso-stage.nylservices.net/update-profile?clientId=6pdeoajlh4ttgktolu3jir8gp6&callbackUri=https://google.com"

        self.verificationErrors = []
        self.accept_next_alert = True

    # The tearDown method will get called after every test method. This is a place to do all cleanup actions.
    def tearDown(self):
        # NOTE: this code for checking for exceptions does NOT work for Safari
        # Python 3.8+ may have this built in. Need to revisit at future date.
        # checking for exceptions or assertion errors, if there are take screenshot
        # for method, error in self._outcome.errors:
        #     if error:
        #         funct.fullshot(self.driver)
        #         funct.generateHAR(self.server, self.driver)
        # # self.driver.quit()
        self.assertEqual([], self.verificationErrors)

##Test Runner:
# In python3 you can run discover mode from the terminal without any code changes, the code to run is as folloew:
# $python3 -m unittest discover -s <project_directory> -p "<starting_syntax>*.py"
# EG:
# $python3 -m unittest discover -s nyl/ -p "reg*.py"
# would, assuming you were in the QA/ directory, run all test-cases on all files that began with "reg" in the nyl/ folder