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
    def test01_updateFName(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        fnameChange = 'Arthur'
        funct.clearTextField(driver, var.updateProfV.fname)
        funct.waitAndSend(driver, var.updateProfV.fname, fnameChange)
        funct.waitAndClick(driver, var.updateProfV.update_button)
        time.sleep(2)
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
        change = driver.find_element(var.updateProfV.fname[0], var.updateProfV.fname[1])
        if funct.checkValue(driver, var.updateProfV.fname, fnameChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.fname[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.fname, fnameChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.fname[2] + ' field should say "' + fnameChange + '" , but says "' + change.get_attribute(
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

# Checks Last name change in update profile saves and redirects successfully
    def test02_updateLName(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        lnameChange = 'Doyle'
        funct.clearTextField(driver, var.updateProfV.lname)
        funct.waitAndSend(driver, var.updateProfV.lname, lnameChange)
        funct.waitAndClick(driver, var.updateProfV.update_button)
        time.sleep(2)
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
        change = driver.find_element(var.updateProfV.lname[0], var.updateProfV.lname[1])
        if funct.checkValue(driver, var.updateProfV.lname, lnameChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.lname[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.lname, lnameChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.lname[2] + ' field should say "' + lnameChange + '" , but says "' + change.get_attribute(
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

# Checks First name + Last name change in update profile saves and redirects successfully
    def test03_updateFNameLName(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        elems = [var.updateProfV.fname, var.updateProfV.lname]
        fnameChange = 'Arthur'
        lnameChange = 'Doyle'
        changes = [fnameChange, lnameChange]
        funct.clearTextField(driver, var.updateProfV.fname)
        funct.waitAndSend(driver, var.updateProfV.fname, fnameChange)
        funct.clearTextField(driver, var.updateProfV.lname)
        funct.waitAndSend(driver, var.updateProfV.lname, lnameChange)
        funct.waitAndClick(driver, var.updateProfV.update_button)
        time.sleep(2)
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
        passedFlags = []
        failedFlags = []
        for e, c in zip(elems, changes):
            elem = driver.find_element(e[0], e[1])
            if funct.checkValue(driver, e, c) == True:
                passedFlags.append(e[2])
                print('PASS - Profile update change for ' + e[2] + ' successfully saved to user.')
                print('Updated text is "' + elem.get_attribute("value") + '"')
            elif funct.checkValue(driver, e, c) == False:
                failedFlags.append(e[2])
                funct.fullshot(driver)
        if len(failedFlags) > 0:
            print('FAIL - Fields below failed to save changes: ')
            print(failedFlags)
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

# 20201002 Note: System does not currently save the Suffix
# Checks Suffix change in update profile saves and redirects successfully
#     def test04_updateLName(self, testemail='self.testemail'):
#         if testemail == 'self.testemail':
#             testemail = self.testemail
#
#         driver = self.driver
#
#         funct.createVerifiedUser(self, testemail)
#         # url is pulled from confTest
#         driver.get(self.update_url)
#         time.sleep(2)
#         # Makes change in field and submits
#         suffixChange = 'Jr'
#         funct.waitAndClick(driver, var.regV.suffix_dropdown)
#         select_box = driver.find_element_by_name("suffix")
#         options = [x for x in select_box.find_elements_by_tag_name("option")]
#         for element in options:
#             if element.text == suffixChange:
#                 element.click()
#                 break
#         funct.waitAndClick(driver, var.updateProfV.update_button)
#         time.sleep(2)
#         # check for proper redirect to Google.com
#         if driver.find_elements_by_name("q") != []:
#             print('Update profile successfully redirected to Google.')
#         else:
#             funct.fullshot(driver)
#             print('FAIL - Update profile redirect screen not reached. Test can not proceed.')
#             try:
#                 funct.purge(self, testemail)
#                 print('test user purged')
#             except:
#                 print('no test user found')
#             print("Test complete!")
#             raise Exception('Update profile redirected incorrectly')
#         # Checks the change has been saved to the profile
#         driver.get(self.update_url)
#         time.sleep(5)
#         change = driver.find_element(var.updateProfV.suffix[0], var.updateProfV.suffix[1])
#         if funct.checkValue(driver, var.updateProfV.suffix, suffixChange) == True:
#             print('PASS - Profile update change for ' + var.updateProfV.suffix[2] + ' successfully saved to user.')
#             print('Updated text is "' + change.get_attribute("value") + '"')
#         elif funct.checkValue(driver, var.updateProfV.suffix, suffixChange) == False:
#             print(
#                 'FAIL - Updated ' + var.updateProfV.suffix[2] + ' field should say "' + suffixChange + '" , but says "' + change.get_attribute(
#                     "value") + '"!')
#             funct.fullshot(driver)
#             try:
#                 funct.purge(self, testemail)
#                 print('test user purged')
#             except:
#                 print('no test user found')
#             print("Test complete!")
#             raise Exception('Update profile changes failed to save.')
#
#         # Deleting test data
#         try:
#             funct.purge(self, testemail)
#             print('test user purged')
#         except:
#             print('no test user found')
#         print("Test complete!")
#
# 20201002 Note: System does not currently save the Suffix
# Checks First name + Last name + Suffix change in update profile saves and redirects successfully
#     def test05_updateFNameLNameSuffix(self, testemail='self.testemail'):
#         if testemail == 'self.testemail':
#             testemail = self.testemail
#
#         driver = self.driver
#
#         funct.createVerifiedUser(self, testemail)
#         # url is pulled from confTest
#         driver.get(self.update_url)
#         time.sleep(2)
#         # Makes change in field and submits
#         elems = [var.updateProfV.fname, var.updateProfV.lname, var.updateProfV.suffix]
#         fnameChange = 'Arthur'
#         lnameChange = 'Doyle'
#         suffixChange = 'Jr'
#         changes = [fnameChange, lnameChange, suffixChange]
#         funct.clearTextField(driver, var.updateProfV.fname)
#         funct.waitAndSend(driver, var.updateProfV.fname, fnameChange)
#         funct.clearTextField(driver, var.updateProfV.lname)
#         funct.waitAndSend(driver, var.updateProfV.lname, lnameChange)
#         funct.waitAndClick(driver, var.regV.suffix_dropdown)
#         select_box = driver.find_element_by_name("suffix")
#         options = [x for x in select_box.find_elements_by_tag_name("option")]
#         for element in options:
#             if element.text == suffixChange:
#                 element.click()
#                 break
#         funct.waitAndClick(driver, var.updateProfV.update_button)
#         time.sleep(2)
#         # check for proper redirect to Google.com
#         if driver.find_elements_by_name("q") != []:
#             print('Update profile successfully redirected to Google.')
#         else:
#             funct.fullshot(driver)
#             print('FAIL - Update profile redirect screen not reached. Test can not proceed.')
#             try:
#                 funct.purge(self, testemail)
#                 print('test user purged')
#             except:
#                 print('no test user found')
#             print("Test complete!")
#             raise Exception('Update profile redirected incorrectly')
#
#         # Checks the change has been saved to the profile
#         driver.get(self.update_url)
#         time.sleep(5)
#         passedFlags = []
#         failedFlags = []
#         for e, c in zip(elems, changes):
#             # elem = driver.find_element(e[0], e[1])
#             if funct.checkValue(driver, e, c) == True:
#                 passedFlags.append(e[2])
#                 print('PASS - Profile update change for ' + e[1] + ' successfully saved to user.')
#             elif funct.checkValue(driver, e, c) == False:
#                 failedFlags.append(e[2])
#                 funct.fullshot(driver)
#         if len(failedFlags) > 0:
#             print('FAIL - Fields below failed to save changes: ')
#             print(failedFlags)
#             try:
#                 funct.purge(self, testemail)
#                 print('test user purged')
#             except:
#                 print('no test user found')
#             print("Test complete!")
#             raise Exception('Update profile changes failed to save.')
#
#         # Deleting test data
#         try:
#             funct.purge(self, testemail)
#             print('test user purged')
#         except:
#             print('no test user found')
#         print("Test complete!")

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))