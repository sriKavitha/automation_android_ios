# [Documentation - Setup] This section lists all dependencies
# that are imported for variable file to work
from selenium.webdriver.common.by import By
import funct, confTest
# [Documentation - Summary] This file creates the variables for
# NYL Admin Dashboard objects for testing user flows

# Credentials for NYL Admin Dashboard
class CREDSadmin:
    # obtain creds file from the 1Password QA vault (contact QA lead on project for access)
    # opens specific local creds file with user data according to confTest variable
    if confTest.NYLadminBASE.testdata == 'iddw':
        notepadfile = open('/Users/Shared/testing/andrewpii.txt', 'r')
    elif confTest.NYLadminBASE.testdata == 'real':
        notepadfile = open('/Users/Shared/testing/nyl08022021.txt', 'r')
    # turns variable into a list of every line in above notepadfile
    entry_info = notepadfile.read().splitlines()
    superadmin_username = funct.getCredential(entry_info, 'admin-super-un')
    superadmin_psw = funct.getCredential(entry_info, 'admin-super-psw')

# [Documentation - Variables] Elements on Login page
class loginV:
    email = [By.XPATH, '(//input[@id="signInFormUsername"])[2]', 'email']
    password = [By.XPATH, '(//input[@id="signInFormPassword"])[2]', 'password']
    forgotPassword_link = [By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div/form/a', 'forgotPassword_link']
    signin_button = [By.XPATH, '(//input[@name="signInSubmitButton"])[2]', 'signin_button']

# [Documentation - Variables] Elements on Dashboard pages
class dashV:
    home_breadcrumb_link = [By.XPATH, '//*[@id="kt_subheader"]/div/div/div/a[1]', 'home_breadcrumb_link']
    users_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[1]/a/span', 'users_link']
    pendingDeletion_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[2]/a/span', 'pendingDeletion_link']
    permanentlyDeleted_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[3]/a/span', 'permanentlyDeleted_link']
    admins_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[4]/a/span', 'admins_link']
    features_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[5]/a/span', 'features_link']
    search_input = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/input', 'search_input']
    category_email = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[2]/a', 'category_email']
    operator_contains = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[2]/a', 'operator_contains']
    search_button = [By.CSS_SELECTOR, '#kt_content > div.kt-container.kt-container--fluid.kt-grid__item.kt-grid__item--fluid > div > div > div > div.kt-portlet__body > div:nth-child(1) > div > div > div > div > div > div > div.form-group > button', 'signin_button']
    bulkAction_button = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/button', 'bulkAction_button']
    li_verification = [By.XPATH, '/html/body/div[2]/div/div/ul/li[1]', "li_verification"]
    li_unverification = [By.XPATH, '/html/body/div[2]/div/div/ul/li[2]', "li_unverification"]
    li_lock = [By.XPATH, '/html/body/div[2]/div/div/ul/li[3]', "li_lock"]
    li_unlock = [By.XPATH, '/html/body/div[2]/div/div/ul/li[4]', "li_unlock"]
    li_delete = [By.XPATH, '/html/body/div[2]/div/div/ul/li[5]', "li_delete"]
    comment_textarea = [By.XPATH, '//textarea[@id="comment"]', 'comment_textarea']
    comment_phrase_textarea = [By.XPATH, '//input[@id="phrase"]', 'comment_phrase_textarea']
    modal_ok_button = [By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]', 'modal_ok_button']
    returnedUser_checkbox = [By.XPATH, '(//input[@type="checkbox"])[2]', 'returnedUser_checkbox']
    no_data_msg = [By.XPATH, '//*[@id="local_data"]/div/div/div/div/div/div/table/tbody/tr/td/div/p', 'no_data_msg']
