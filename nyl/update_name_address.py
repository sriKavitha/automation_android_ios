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

# 20201002 Note: System does not currently save the Suffix
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

# Checks House Number change in update profile saves and redirects successfully
    def test04_updateHouse(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        houseChange = '123'
        funct.clearTextField(driver, var.updateProfV.housenum)
        funct.waitAndSend(driver, var.updateProfV.housenum, houseChange)
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
        change = driver.find_element(var.updateProfV.housenum[0], var.updateProfV.housenum[1])
        if funct.checkValue(driver, var.updateProfV.housenum, houseChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.housenum[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.housenum, houseChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.fname[1] + ' field should say "' + houseChange + '" , but says "' + change.get_attribute(
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

# Checks Street Name change in update profile saves and redirects successfully
    def test05_updateStreet(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        streetChange = 'First Street'
        funct.clearTextField(driver, var.updateProfV.street)
        funct.waitAndSend(driver, var.updateProfV.street, streetChange)
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
        change = driver.find_element(var.updateProfV.street[0], var.updateProfV.street[1])
        if funct.checkValue(driver, var.updateProfV.street, streetChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.street[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.street, streetChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.street[2] + ' field should say "' + streetChange + '" , but says "' + change.get_attribute(
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

# Checks Apartment change in update profile saves and redirects successfully
    def test06_updateApt(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        aptChange = '2B'
        funct.clearTextField(driver, var.updateProfV.add2)
        funct.waitAndSend(driver, var.updateProfV.add2, aptChange)
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
        change = driver.find_element(var.updateProfV.add2[0], var.updateProfV.add2[1])
        if funct.checkValue(driver, var.updateProfV.add2, aptChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.add2[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.add2, aptChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.add2[2] + ' field should say "' + aptChange + '" , but says "' + change.get_attribute(
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

# Checks City change in update profile saves and redirects successfully
    def test07_updateCity(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        cityChange = 'Anytown'
        funct.clearTextField(driver, var.updateProfV.city)
        funct.waitAndSend(driver, var.updateProfV.city, cityChange)
        funct.waitAndClick(driver, var.updateProfV.update_button)
        time.sleep(2)
        # check for proper redirect to Google.com
        if driver.find_elements_by_name("q") != []:
            print('UUpdate profile successfully redirected to Google.')
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
        change = driver.find_element(var.updateProfV.city[0], var.updateProfV.city[1])
        if funct.checkValue(driver, var.updateProfV.city, cityChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.city[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.city, cityChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.city[2] + ' field should say "' + cityChange + '" , but says "' + change.get_attribute(
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

# Checks State change in update profile saves and redirects successfully
    def test08_updateState(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        stateChange = 'PA'
        funct.waitAndClick(driver, var.updateProfV.state_dropdown)
        select_box = driver.find_element_by_name("state")
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text == stateChange:
                element.click()
                break
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
        change = driver.find_element(var.updateProfV.state_dropdown[0], var.updateProfV.state_dropdown[1])
        if funct.checkValue(driver, var.updateProfV.state_dropdown, stateChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.state_dropdown[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.state_dropdown, stateChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.state_dropdown[2] + ' field should say "' + stateChange + '" , but says "' + change.get_attribute(
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

# Checks Zip change in update profile saves and redirects successfully
    def test09_updateZip(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        zipChange = '11222'
        funct.clearTextField(driver, var.updateProfV.zip)
        funct.waitAndSend(driver, var.updateProfV.zip, zipChange)
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
        change = driver.find_element(var.updateProfV.zip[0], var.updateProfV.zip[1])
        if funct.checkValue(driver, var.updateProfV.zip, zipChange) == True:
            print('PASS - Profile update change for ' + var.updateProfV.zip[2] + ' successfully saved to user.')
            print('Updated text is "' + change.get_attribute("value") + '"')
        elif funct.checkValue(driver, var.updateProfV.zip, zipChange) == False:
            print(
                'FAIL - Updated ' + var.updateProfV.zip[2] + ' field should say "' + zipChange + '" , but says "' + change.get_attribute(
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

# Checks House + Street + City + Zip Address change in update profile saves and redirects successfully
    def test10_updateHSCZ(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        elems = [var.updateProfV.housenum, var.updateProfV.street, var.updateProfV.city, var.updateProfV.zip]
        houseChange = '123'
        streetChange = 'First Street'
        cityChange = 'Anytown'
        zipChange = '11222'
        changes = [houseChange, streetChange, cityChange, zipChange]
        funct.clearTextField(driver, var.updateProfV.housenum)
        funct.waitAndSend(driver, var.updateProfV.housenum, houseChange)
        funct.clearTextField(driver, var.updateProfV.street)
        funct.waitAndSend(driver, var.updateProfV.street, streetChange)
        funct.clearTextField(driver, var.updateProfV.city)
        funct.waitAndSend(driver, var.updateProfV.city, cityChange)
        funct.clearTextField(driver, var.updateProfV.zip)
        funct.waitAndSend(driver, var.updateProfV.zip, zipChange)

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
                passedFlags.append(e[1])
                print('PASS - Profile update change for ' + e[1] + ' successfully saved to user.')
                print('Updated text is "' + elem.get_attribute("value") + '"')
            elif funct.checkValue(driver, e, c) == False:
                failedFlags.append(e[1])
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

# Checks House + Street + Apt + City + Zip Address change in update profile saves and redirects successfully
    def test11_updateHSACZ(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        elems = [var.updateProfV.housenum, var.updateProfV.street, var.updateProfV.add2, var.updateProfV.city, var.updateProfV.zip]
        houseChange = '123'
        streetChange = 'First Street'
        aptChange = '2B'
        cityChange = 'Anytown'
        zipChange = '11222'
        changes = [houseChange, streetChange, aptChange, cityChange, zipChange]
        funct.clearTextField(driver, var.updateProfV.housenum)
        funct.waitAndSend(driver, var.updateProfV.housenum, houseChange)
        funct.clearTextField(driver, var.updateProfV.street)
        funct.waitAndSend(driver, var.updateProfV.street, streetChange)
        funct.clearTextField(driver, var.updateProfV.add2)
        funct.waitAndSend(driver, var.updateProfV.add2, aptChange)
        funct.clearTextField(driver, var.updateProfV.city)
        funct.waitAndSend(driver, var.updateProfV.city, cityChange)
        funct.clearTextField(driver, var.updateProfV.zip)
        funct.waitAndSend(driver, var.updateProfV.zip, zipChange)
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
                passedFlags.append(e[1])
                print('PASS - Profile update change for ' + e[1] + ' successfully saved to user.')
                print('Updated text is "' + elem.get_attribute("value") + '"')
            elif funct.checkValue(driver, e, c) == False:
                failedFlags.append(e[1])
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

# Checks House + Street + City + State + Zip Address change in update profile saves and redirects successfully
    def test12_updateHSCSZ(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        elems = [var.updateProfV.housenum, var.updateProfV.street, var.updateProfV.city, var.updateProfV.state_dropdown, var.updateProfV.zip]
        houseChange = '123'
        streetChange = 'First Street'
        cityChange = 'Anytown'
        stateChange = 'PA'
        zipChange = '11222'
        changes = [houseChange, streetChange, cityChange, stateChange, zipChange]
        funct.clearTextField(driver, var.updateProfV.housenum)
        funct.waitAndSend(driver, var.updateProfV.housenum, houseChange)
        funct.clearTextField(driver, var.updateProfV.street)
        funct.waitAndSend(driver, var.updateProfV.street, streetChange)
        funct.clearTextField(driver, var.updateProfV.city)
        funct.waitAndSend(driver, var.updateProfV.city, cityChange)
        funct.waitAndClick(driver, var.updateProfV.state_dropdown)
        select_box = driver.find_element_by_name("state")
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text == stateChange:
                element.click()
                break
        funct.clearTextField(driver, var.updateProfV.zip)
        funct.waitAndSend(driver, var.updateProfV.zip, zipChange)
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

# Checks common use case, Last Name + House + Street + Apt + City + State + Zip Address change in update profile saves and redirects successfully
    def test13_updateLHSACSZ(self, testemail='self.testemail'):
        if testemail == 'self.testemail':
            testemail = self.testemail

        driver = self.driver

        funct.createVerifiedUser(self, testemail)
        # url is pulled from confTest
        driver.get(self.update_url)
        time.sleep(2)
        # Makes change in field and submits
        elems = [var.updateProfV.lname, var.updateProfV.housenum, var.updateProfV.street, var.updateProfV.add2, var.updateProfV.city, var.updateProfV.state_dropdown, var.updateProfV.zip]
        lnameChange = 'Smith'
        houseChange = '123'
        streetChange = 'First Street'
        aptChange = '2B'
        cityChange = 'Anytown'
        stateChange = 'PA'
        zipChange = '11222'
        changes = [lnameChange, houseChange, streetChange, aptChange, cityChange, stateChange, zipChange]
        funct.clearTextField(driver, var.updateProfV.lname)
        funct.waitAndSend(driver, var.updateProfV.lname, lnameChange)
        funct.clearTextField(driver, var.updateProfV.housenum)
        funct.waitAndSend(driver, var.updateProfV.housenum, houseChange)
        funct.clearTextField(driver, var.updateProfV.street)
        funct.waitAndSend(driver, var.updateProfV.street, streetChange)
        funct.clearTextField(driver, var.updateProfV.add2)
        funct.waitAndSend(driver, var.updateProfV.add2, aptChange)
        funct.clearTextField(driver, var.updateProfV.city)
        funct.waitAndSend(driver, var.updateProfV.city, cityChange)
        funct.waitAndClick(driver, var.updateProfV.state_dropdown)
        select_box = driver.find_element_by_name("state")
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text == stateChange:
                element.click()
                break
        funct.clearTextField(driver, var.updateProfV.zip)
        funct.waitAndSend(driver, var.updateProfV.zip, zipChange)
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


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))