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
    email = [By.ID, "signInFormUsername", "email"]
    password = [By.ID, "signInFormPassword", "password"]
    forgot_password_link = [By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div/form/a", "forgot_password_link"]
    signin_button = [By.NAME, "signInSubmitButton", "signin_button"]

# [Documentation - Variables] Elements on Home Dashboard page
# class homeDashV:
