# [Documentation - Setup] This section lists all dependencies
# that are imported for variable file to work
from selenium.webdriver.common.by import By
import funct
# [Documentation - Summary] This file creates the variables for
# NYL App objects for testing user flows

# [Documentation - Variables] Objects on Registration page

# Credentials for NYL Services API
class CREDSapi:
    # opens local file with user data
    notepadfile = open('/Users/Shared/testing/nyl06102020.txt', 'r')
    # turns variable into a list of every line in above notepadfile
    entry_info = notepadfile.read().splitlines()
    devCID = funct.getCredential(entry_info, 'Nyl-Services-client-id-dev')
    devXKEY = funct.getCredential(entry_info, 'Nyl-services-api-key-dev')
    qaCID = funct.getCredential(entry_info, 'Nyl-Services-client-id-qa')
    qaXKEY = funct.getCredential(entry_info, 'Nyl-services-api-key-qa')
    stageCID = funct.getCredential(entry_info, 'Nyl-Services-client-id-stage')
    stageXKEY = funct.getCredential(entry_info, 'Nyl-services-api-key-stage')
    fname = funct.getCredential(entry_info, 'first-name')
    lname = funct.getCredential(entry_info, 'last-name')
    hnum = funct.getCredential(entry_info, 'house-number')
    street = funct.getCredential(entry_info, 'street-address')
    city = funct.getCredential(entry_info, 'city')
    state = funct.getCredential(entry_info, 'state')
    zip = funct.getCredential(entry_info, 'zip')
    pnum = funct.getCredential(entry_info, 'Phone-number')
    ssn = funct.getCredential(entry_info, 'ssn')
    dob_month = funct.getCredential(entry_info, 'dob-month')
    dob_date = funct.getCredential(entry_info, 'dob-date')
    dob_year = funct.getCredential(entry_info, 'dob-year')
    password = funct.getCredential(entry_info, 'password')
    mobileUN = funct.getCredential(entry_info, 'mobile-un')
    mobilePW = funct.getCredential(entry_info, 'mobile-pw')
