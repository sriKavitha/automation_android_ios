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
    notepadfile = open('/Users/Shared/testing/api10292020.txt', 'r')
    # turns variable into a list of every line in above notepadfile
    entry_info = notepadfile.read().splitlines()

    ssoFName = funct.getCredential(entry_info, 'sso-first-name')
    ssoLName = funct.getCredential(entry_info, 'sso-last-name')
    ssoHNum = funct.getCredential(entry_info, 'sso-house-number')
    ssoStreet = funct.getCredential(entry_info, 'sso-street-address')
    ssoCity = funct.getCredential(entry_info, 'sso-city')
    ssoState = funct.getCredential(entry_info, 'sso-state')
    ssoZip = funct.getCredential(entry_info, 'sso-zip')
    ssoPhone = funct.getCredential(entry_info, 'sso-phone')
    ssoSSN = funct.getCredential(entry_info, 'sso-ssn')
    ssoDOBmonth = funct.getCredential(entry_info, 'sso-dob-month')
    ssoDOBDate = funct.getCredential(entry_info, 'sso-dob-date')
    ssoDOBYear = funct.getCredential(entry_info, 'sso-dob-year')
    ssoPW = funct.getCredential(entry_info, 'sso-test-password')
    mobileFName = funct.getCredential(entry_info, 'mobile-first-name')
    mobileLName = funct.getCredential(entry_info, 'mobile-last-name')
    mobilePhone = funct.getCredential(entry_info, 'mobile-phone')
    mobilePW = funct.getCredential(entry_info, 'mobile-test-password')
    devSSOcid = funct.getCredential(entry_info, 'nyl-services-client-id-dev')
    qaSSOcid = funct.getCredential(entry_info, 'nyl-services-client-id-qa')
    stageSSOcid = funct.getCredential(entry_info, 'nyl-services-client-id-stage')
    devSSOxkey = funct.getCredential(entry_info, 'nyl-services-x-api-key-dev')
    qaSSOxkey = funct.getCredential(entry_info, 'nyl-services-x-api-key-qa')
    stageSSOxkey = funct.getCredential(entry_info, 'nyl-services-x-api-key-stage')
    devSSOhgcode = funct.getCredential(entry_info, 'sso-handle-govid-code-dev')
    qaSSOhgcode = funct.getCredential(entry_info, 'sso-handle-govid-code-qa')
    devMOBILEcid = funct.getCredential(entry_info, 'mobile-client-id-dev')
    qaMOBILEcid = funct.getCredential(entry_info, 'mobile-client-id-qa')
    stageMOBILEcid = funct.getCredential(entry_info, 'mobile-client-id-stage')
    devMOBILExkey = funct.getCredential(entry_info, 'mobile-x-api-key-dev')
    qaMOBILExkey = funct.getCredential(entry_info, 'mobile-x-api-key-qa')
    stageMOBILExkey = funct.getCredential(entry_info, 'mobile-x-api-key-stage')
    devFCMtoken = funct.getCredential(entry_info, 'mobile-fcm-token-dev')
    qaFCMtoken = funct.getCredential(entry_info, 'mobile-fcm-token-qa')
    stageFCMtoken = funct.getCredential(entry_info, 'mobile-fcm-token-stage')

