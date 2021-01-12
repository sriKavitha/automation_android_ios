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
        self.env = 'stage'

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