# [Documentation - Setup] This section lists all dependencies
# that are imported for function file to work
import json
import time
from urllib.parse import urlparse

import boto3
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import util
import var

# [Documentation - Summary] This file creates the functions for
# use in the automation test suite of NYL

# [Documentation - Function] Checks for existing test user email in SSO userpool
# and if found deletes the user through the Admin Dashboard.
def purgeSSOemail(self, email):
    if self.env == 'dev':
        self.admin_url = 'https://admin-dev.nylservices.net/'
    elif self.env == 'qa':
        self.admin_url = 'https://admin-qa.nylservices.net/'
    elif self.env == 'stage':
        self.admin_url = 'https://admin-stage.nylservices.net/'
    driver = self.driver
    driver.get(self.admin_url)
    testemail = email
    # Instructions for webdriver to read and input user data via the info on the .txt doc.
    # Credentials are localized to one instance via the var file
    try:  # try to login
        waitAndSend(driver, var.adminLoginVar.email, var.CREDSadmin.superadmin_username)
        waitAndSend(driver, var.adminLoginVar.password, var.CREDSadmin.superadmin_psw)
        waitAndClick(driver, var.adminLoginVar.signin_button)
    except Exception:  # if session persists from before, extend session and continue
        try:
            waitAndClick(driver, var.adminDashVar.extend_button)
            print('Admin Dash Session persisted, login bypassed')
        except:
            pass
    # Search for test user via Email
    # TODO due to ongoing Admin Dash work in dev env, this if else is in place,
    #  will need to update once AD work is complete
    if self.env == 'dev':
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndSend(driver, var.adminDashVar.search_input, testemail)
    else:
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndClick(driver, var.adminDashVar.category_email)
        waitAndClick(driver, var.adminDashVar.operator_contains)
        waitAndSend(driver, var.adminDashVar.search_input, testemail)
        driver.find_element_by_xpath(var.adminDashVar.search_input[1]).send_keys(Keys.ENTER)
    try:
        time.sleep(2)
        waitAndClick(driver, var.adminDashVar.search_button)
        waitAndClick(driver, var.adminDashVar.search_button)
    except:
        time.sleep(2)
        try:
            waitAndClick(driver, var.adminDashVar.search_button)
        except:
            waitAndClick(driver, var.adminDashVar.search_button)

    time.sleep(5)
    # Checks the returned user is the correct user
    rows = []
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if len(rows) == 1:
        if driver.find_element_by_xpath('//td[@class="ant-table-cell"][4]').text == testemail:  # email
            pass  # check that first user returned is has the same email address
        else:
            print(f'\nunexpected behavior: please check screenshot')
            fullshot(driver)
    elif len(rows) >= 2:  # more than 1 user was returned in table
        fullshot(driver)
        print(f'\nMore than 1 user found in table, check screenshot')
        raise Exception
    elif driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  # no user returned in table
        print(f'\nno test user {testemail} found')
        # open new window with execute_script()
        driver.execute_script("window.open('');")
        closeWindow(driver, 'New York Lottery - Admin Dashboard')
        exit()
    else:
        print(f'\nunexpected behavior: please check screenshot')
        fullshot(driver)
    # Clicks checkbox for first user returned
    waitAndClick(driver, var.adminDashVar.searchedUser_checkbox)
    waitAndClick(driver, var.adminDashVar.bulkAction_button)
    waitAndClick(driver, var.adminDashVar.li_delete)
    # Submits comment and mandatory text for completion
    ts = timeStamp()
    waitAndSend(driver, var.adminDashVar.comment_textarea, "automated test change at " + ts)
    # attempt to click the modal "OK" buttons to proceed to next step
    # different locator for same button depending on new session or extended session
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    waitAndSend(driver, var.adminDashVar.comment_phrase_textarea, "mark for deletion")
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    time.sleep(2)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    # # Navigates to Pending Deletion user list to purge user
    waitAndClick(driver, var.adminDashVar.pendingDeletion_link)
    time.sleep(2)
    # Search for test user via Email
    # TODO due to ongoing Admin Dash work in dev env, this if else is in place, will need to update once AD work is complete
    if self.env == 'dev':
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndSend(driver, var.adminDashVar.search_input, testemail)
    else:
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndClick(driver, var.adminDashVar.category_email)
        waitAndClick(driver, var.adminDashVar.operator_contains)
        waitAndSend(driver, var.adminDashVar.search_input, testemail)
        driver.find_element_by_xpath(var.adminDashVar.search_input[1]).send_keys(Keys.ENTER)
    # time.sleep(2)
    waitAndClick(driver, var.adminDashVar.search_button)
    time.sleep(5)
    rows = []
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if len(rows) == 1:
        if driver.find_element_by_xpath('//td[@class="ant-table-cell"][4]').text == testemail:  # email
            pass  # check that first user returned is has the same email address
        else:
            print(f'unexpected behavior: please check screenshot')
            fullshot(driver)
    elif len(rows) >= 2:  # more than 1 user was returned in table
        fullshot(driver)
        print(f'More than 1 user found in Pending Deletion list, check screenshot')
        raise Exception
    elif driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  # no user returned in table
        print(f'no test user {testemail} found')
        # open new window with execute_script()
        driver.execute_script("window.open('');")
        closeWindow(driver, 'New York Lottery - Admin Dashboard')
        exit()
    else:
        print(f'unexpected behavior: please check screenshot')
        fullshot(driver)
    # Clicks checkbox for first user returned
    waitAndClick(driver, var.adminDashVar.pendingDeleteUser_checkbox)
    waitAndClick(driver, var.adminDashVar.bulkAction_button)
    waitAndClick(driver, var.adminDashVar.li_permDelete)
    # Submits comment and mandatory text for completion
    ts = timeStamp()
    waitAndSend(driver, var.adminDashVar.comment_textarea, "automated test change at " + ts)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    waitAndSend(driver, var.adminDashVar.comment_phrase_textarea, "purge")
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    time.sleep(2)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            try:
                waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            except:
                try:
                    waitAndClick(driver, var.adminDashVar.extend_button)
                except:
                    pass

    time.sleep(3)
    # Search for test user via Email again to confirm user is gone from system
    waitAndClick(driver, var.adminDashVar.search_button)
    time.sleep(3)
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  #search returns no data
        print(f'\ntest user {testemail} found and purged')
    elif len(rows) >= 1:  # search returns list of users
        fullshot(driver)
        print(f'\nuser still in Pending Deletion list with {testemail}, check user pool')
        raise Exception
    else:
        print(f'\nunexpected behavior: please check screenshot')
        fullshot(driver)

# [Documentation - Function] Checks for existing test user phone number in SSO userpool
# and if found deletes the user through the Admin Dashboard.
def purgeSSOphone(self, phone):
    if self.env == 'dev':
        self.admin_url = 'https://admin-dev.nylservices.net/'
    elif self.env == 'qa':
        self.admin_url = 'https://admin-qa.nylservices.net/'
    elif self.env == 'stage':
        self.admin_url = 'https://admin-stage.nylservices.net/'
    driver = self.driver
    # url is pulled from confTest
    driver.get(self.admin_url)
    testphone = phone
    formatted_phone = '+1 (' + testphone[:3] + ') ' + testphone[3:6] + '-' + testphone[6:]  # match the formatiing in the returned users table: +1 (407) 348-7541
    # Instructions for webdriver to read and input user data via the info on the .txt doc.
    # Credentials are localized to one instance via the var file
    try:
        waitAndSend(driver, var.adminLoginVar.email, var.CREDSadmin.superadmin_username)
        waitAndSend(driver, var.adminLoginVar.password, var.CREDSadmin.superadmin_psw)
        waitAndClick(driver, var.adminLoginVar.signin_button)
    except Exception:  # if session persists from before, extend session and continue
        try:
            waitAndClick(driver, var.adminLoginVar.extend_button)
            print('Admin Dash Session persisted, login bypassed')
        except:
            pass
    # Search for test user via phone
    # TODO due to ongoing Admin Dash work in dev env, this if else is in place, will need to update once AD work is complete
    if self.env == 'dev':
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndSend(driver, var.adminDashVar.search_input, testphone)
    else:
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndClick(driver, var.adminDashVar.category_phone)
        waitAndClick(driver, var.adminDashVar.operator_contains)
        waitAndSend(driver, var.adminDashVar.search_input, testphone)
        driver.find_element_by_xpath(var.adminDashVar.search_input[1]).send_keys(Keys.ENTER)
    try:
        time.sleep(2)
        waitAndClick(driver, var.adminDashVar.search_button)
        waitAndClick(driver, var.adminDashVar.search_button)
    except:
        time.sleep(2)
        try:
            waitAndClick(driver, var.adminDashVar.search_button)
        except:
            waitAndClick(driver, var.adminDashVar.search_button)

    time.sleep(5)
    # Checks the returned user is the correct user
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if len(rows) == 1:
        if driver.find_element_by_xpath('//td[@class="ant-table-cell"][6]').text == formatted_phone:  # phone
            pass  # check that first user returned has the same phone
        else:
            print(f'\nunexpected behavior: please check screenshot')
            fullshot(driver)
    elif len(rows) >= 2:  # more than 1 user was returned in table
        fullshot(driver)
        print(f'\nMore than 1 user returned in table, check screenshot')
        raise Exception
    elif driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  # no user returned in table
        print(f'\nno test user {formatted_phone} found')
        # open new window with execute_script()
        driver.execute_script("window.open('');")
        closeWindow(driver, 'New York Lottery - Admin Dashboard')
        exit()
    else:
        print(f'\nunexpected behavior: please check screenshot')
        fullshot(driver)
    # Clicks checkbox for first user returned
    waitAndClick(driver, var.adminDashVar.searchedUser_checkbox)
    waitAndClick(driver, var.adminDashVar.bulkAction_button)
    waitAndClick(driver, var.adminDashVar.li_delete)
    # Submits comment and mandatory text for completion
    ts = timeStamp()
    waitAndSend(driver, var.adminDashVar.comment_textarea, "automated test change at " + ts)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    waitAndSend(driver, var.adminDashVar.comment_phrase_textarea, "mark for deletion")
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    time.sleep(5)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    # # Navigates to Pending Deletion user list to purge user
    waitAndClick(driver, var.adminDashVar.pendingDeletion_link)
    # Search for test user via phone number
    # TODO due to ongoing Admin Dash work in dev env, this if else is in place, will need to update once AD work is complete
    if self.env == 'dev':
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndSend(driver, var.adminDashVar.search_input, testphone)
    else:
        waitAndClick(driver, var.adminDashVar.search_input)
        waitAndClick(driver, var.adminDashVar.category_phone)
        waitAndClick(driver, var.adminDashVar.operator_contains)
        waitAndSend(driver, var.adminDashVar.search_input, testphone)
        driver.find_element_by_xpath(var.adminDashVar.search_input[1]).send_keys(Keys.ENTER)
    time.sleep(2)
    waitAndClick(driver, var.adminDashVar.search_button)
    time.sleep(3)
    # Checks the returned user is the correct user
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if len(rows) == 1:
        if driver.find_element_by_xpath('//td[@class="ant-table-cell"][6]').text == formatted_phone:  # phone
            pass  # check that first user returned has the same phone
        else:
            print(f'unexpected behavior: please check screenshot')
            fullshot(driver)
    elif len(rows) >= 2:  # more than 1 user was returned in table
        fullshot(driver)
        print(f'More than 1 user found in Pending Deletion list, check screenshot')
        raise Exception
    elif driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  # no user returned in table
        print(f'test user {formatted_phone} NOT found on Pending Deletion list')
        # open new window with execute_script()
        driver.execute_script("window.open('');")
        closeWindow(driver, 'New York Lottery - Admin Dashboard')
        exit()
    else:
        print(f'unexpected behavior: please check screenshot')
        fullshot(driver)
    # Clicks checkbox for first user returned
    waitAndClick(driver, var.adminDashVar.pendingDeleteUser_checkbox)
    waitAndClick(driver, var.adminDashVar.bulkAction_button)
    waitAndClick(driver, var.adminDashVar.li_permDelete)
    # Submits comment and mandatory text for completion
    ts = timeStamp()
    waitAndSend(driver, var.adminDashVar.comment_textarea, "automated test change at " + ts)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    waitAndSend(driver, var.adminDashVar.comment_phrase_textarea, "purge")
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    time.sleep(2)
    try:
        waitAndClick(driver, var.adminDashVar.modal_ok_button)
    except:
        try:
            waitAndClick(driver, var.adminDashVar.ext2_modal_ok_button)
        except:
            waitAndClick(driver, var.adminDashVar.ext1_modal_ok_button)
            pass
    time.sleep(3)
    # Search for test user via Email again to confirm user is gone from system
    waitAndClick(driver, var.adminDashVar.search_button)
    time.sleep(3)
    rows = driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]')
    if driver.find_elements_by_xpath(var.adminDashVar.no_data_msg[1]) != []:  #search returns no data
        print(f'\ntest user {formatted_phone} found and purged')
    elif len(rows) >= 1:  # search returns list of users
        fullshot(driver)
        print(f'\nuser still in Pending Deletion list with {formatted_phone}, check user pool')
        raise Exception
    else:
        print(f'\nunexpected behavior: please check screenshot')
        fullshot(driver)

    # [Documentation - Function] Checks for existing test user in Mobile App userpool and deletes the user if found.
def purgeMobile(self, email):
    if self.env == 'dev':
        userpool = 'us-east-1_OSdCjCmwo'
    elif self.env == 'qa':
        userpool = 'us-east-1_Fwp84k69u'
    elif self.env == 'stage':
        userpool = 'us-east-1_hG2UobNyZ'
    client = boto3.client('cognito-idp')
    # print(userpool)
    testemail = 'email ="' + str(email) + '"'
    response = client.list_users(
        UserPoolId=userpool,
        AttributesToGet=[
            'email',
        ],
        Limit=30,
        Filter=testemail
    )
    # print(response)
    testUser = response['Users'][0]['Username']
    response2 = client.admin_delete_user(
        UserPoolId=userpool,
        Username=testUser
    )
    # print(response2)

# [Documentation - Function] uses a filtering method to more easily get and maintain credentials from the credential page (which is now localized to one instance via the var page)
# target should be given plainly, without colons
def getCredential(list, target):
    targ = str(target + ': ')
    credential = [item for item in list if item.startswith(targ)][0]
    cred = credential.replace(targ, '')
    return cred

# [Documentation - Function] starts a browsermob proxy and generates a har file of current page
def generateHAR(server, driver):
    hurl = str(driver.current_url)
    server = Server("/Users/browsermob-proxy-2.1.4/bin/browsermob-proxy",  options={'port': 8090})
    server.start()
    proxy = server.create_proxy()
    chromedriver = "/usr/local/bin/chromedriver"
    url = urlparse(proxy.proxy).path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(url))
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    proxy.new_har("test", options={'captureHeaders': True})
    driver.get(hurl)
    result = json.dumps(proxy.har, ensure_ascii=False)
    print(result)
    harname = str('HAR_' + timeStamp())
    with open(harname, 'w') as har_file:
        json.dump(proxy.har, har_file)
    proxy.close()

# [Documentation - Function] Webdriver uses actionchains to  wait for a specified page element
def waitUntil(browser, elem):
    a = ActionChains(browser)
    try:
        a.move_to_element(browser.find_element(elem[0], elem[1])).perform()
        assert(browser.find_element(elem[0], elem[1]))
    except:
        time.sleep(2)
        try:
            a.move_to_element(browser.find_element(elem[0], elem[1])).perform()
            assert(browser.find_element(elem[0], elem[1]))
        except:
            print("E--" + elem[1] + " elem not found")

# [Documentation - Function] Webdriver waits for a specified page element
# to appear and then proceeds to click on it
def waitAndClick(browser, elem):
    waitUntil(browser, elem)
    browser.find_element(elem[0], elem[1]).click()

# [Documentation - Function] Webdriver waits for a specified page element
# to appear and then proceeds to send keys to it
def waitAndSend(browser, elem, keys):
    waitUntil(browser, elem)
    browser.find_element(elem[0], elem[1]).send_keys(keys)

def clearTextField(browser, elem):
    waitUntil(browser, elem)
    browser.find_element(elem[0], elem[1]).clear()

# [Documentation - Function] Function that grabs UTC time and converts to human readable format
def timeStamp():
    ts = time.gmtime()
    times = time.strftime("%Y-%m-%d_%H-%M-%S", ts)
    return times

# [Documentation - Function] Function that checks the text of a given element against a given stub
def checkText(browser, elem, stub):
    waitUntil(browser, elem)
    el = browser.find_element(elem[0], elem[1])
    if el.text == stub:
        assert el.text == stub
    else:
        print('E---Text Incorrect!\n\nExpected text: "' + stub + '"\n\n but text was: "' + el.text + '"')
        assert el.text == stub

# [Documentation - Function] Function that calls the script to grab full page UTC timestamped screenshot
def fullshot(browser):
    browser.set_window_position(0, 0)
    browser.maximize_window()
    timestamp = timeStamp() + '.png'
    util.fullpage_screenshot(browser, timestamp)

# [Documentation - Function] Checks that an error exists
def checkError(browser, elemWarning):
    try:
        browser.find_element(elemWarning[0], elemWarning[1])
        return True
    except:
        return False

# [Documentation - Function] Checks the actual warning text against the reported warning copy
def checkErrorText(browser, elemWarning, elemWarningStub):
    warning = browser.find_element(elemWarning[0], elemWarning[1])
    if warning.get_attribute("innerText") == elemWarningStub:
        return True
    else:
        return False


# [Documentation - Function] Checks the actual value in the field against the expected value
def checkValue(browser, elem, valueExpected):
    warning = browser.find_element(elem[0], elem[1])
    if warning.get_attribute("value") == valueExpected:
        return True
    else:
        return False

# [Documentation - Function] Creates a verified user that has the following flags:
# # custom:ssn_verification	"Y"
# # custom:phone_verification	"Y"
# # custom:gov_id_verification	"X"
# # custom:verified	"Y"
def createVerifiedUser(self, email):
        # Check for existing test user and wipe it from userpool prior to test execution
        try:
            purgeSSOemail(self, email)
            print('test user purged')
        except:
            print('no test user found')
        driver = self.driver
        driver.get(self.reg_url)
        # Instructions for webdriver to read and input user data via the info on the .txt doc.
        # Credentials are localized to one instance via the var file
        waitAndSend(driver, var.regV.fname, var.credsSSOWEB.fname)
        waitAndSend(driver, var.regV.lname, var.credsSSOWEB.lname)
        waitAndSend(driver, var.regV.housenum, var.credsSSOWEB.housenum)
        waitAndSend(driver, var.regV.street, var.credsSSOWEB.street)
        waitAndSend(driver, var.regV.city, var.credsSSOWEB.city)
        # Find and select the state according to the info in the .txt doc
        # Uses a for loop to iterate through the list of states until element
        # matches the entry info in the text file. Then clicks the element found.
        select_box = driver.find_element_by_name("state")
        waitAndClick(driver, var.regV.state_dropdown)
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        for element in options:
            if element.text in var.credsSSOWEB.state:
                element.click()
                break
        waitAndSend(driver, var.regV.zip, var.credsSSOWEB.zip)
        waitAndSend(driver, var.regV.phone, var.credsSSOWEB.phone)
        waitAndSend(driver, var.regV.ssn4, var.credsSSOWEB.ssn4)
        waitAndSend(driver, var.regV.dob, (
                var.credsSSOWEB.dob_month + var.credsSSOWEB.dob_date + var.credsSSOWEB.dob_year))
        waitAndClick(driver, var.regV.dob_check)
        waitAndSend(driver, var.regV.email, email)
        waitAndSend(driver, var.regV.password, var.credsSSOWEB.password)
        waitAndSend(driver, var.regV.confirmPsw, var.credsSSOWEB.password)
        waitAndClick(driver, var.regV.tos_check)
        waitAndClick(driver, var.regV.submit_button)
        # 2nd screen. OTP selection screen
        waitAndClick(driver, var.otpV.text_button)
        # 3rd screen. OTP code entry screen
        waitAndSend(driver, var.otpV.otp_input, "111111")
        waitAndClick(driver, var.otpV.otp_continue_button)
        time.sleep(5)
        # 4th screen. Successful registration should redirect to Google.com.
        # Checking that the search field on google.com is present on page.
        if driver.find_elements_by_name("q") != []:
            print('Verified user registration is successful.')
        else:
            fullshot(driver)
            print('FAIL - User registration redirect screen not reached. Test can not proceed')
            raise Exception('Registration redirected incorrectly')

def closeWindow(driver, title):
    # return all handles value of open browser window
    handles = driver.window_handles

    for i in handles:
        driver.switch_to.window(i)

        # close specified web page
        if driver.title == title:
            time.sleep(2)
            driver.close()