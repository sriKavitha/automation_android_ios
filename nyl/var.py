# [Documentation - Setup] This section lists all dependencies
# that are imported for variable file to work
from selenium.webdriver.common.by import By

import funct, confTest

###==============================================================###
# NYL Admin Dash
###==============================================================###
# [Documentation - Summary] This section creates the variables for
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
class adminLoginVar:
    email = [By.XPATH, '(//input[@id="signInFormUsername"])[2]', 'email_field']
    password = [By.XPATH, '(//input[@id="signInFormPassword"])[2]', 'password_field']
    forgotPassword_link = [By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div/form/a', 'forgotPassword_link']
    signin_button = [By.XPATH, '(//input[@name="signInSubmitButton"])[2]', 'signin_button']

# [Documentation - Variables] Elements on Dashboard pages
class adminDashVar:
    home_breadcrumb_link = [By.XPATH, '//*[@id="kt_subheader"]/div/div/div/a[1]', 'home_breadcrumb_link']
    users_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[1]/a/span', 'users_link']
    pendingDeletion_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[2]/a/span', 'pendingDeletion_link']
    permanentlyDeleted_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[3]/a/span', 'permanentlyDeleted_link']
    admins_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[4]/a/span', 'admins_link']
    features_link = [By.XPATH, '//*[@id="kt_aside_menu"]/ul/li[5]/a/span', 'features_link']
    # TODO due to ongoing Admin Dash work in dev env, different locators are used for same element, will need to update once AD work is complete
    if confTest.globalVar.env == 'dev':
        search_input = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/input', 'search_input']
    else:
        search_input = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/input', 'search_input']
    category_fname = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[2]/a', 'category_fname']
    category_lname = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[3]/a', 'category_lname']
    category_address = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[4]/a', 'category_address']
    category_phone = [By.XPATH,
                      '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[5]/a',
                      'category_phone']
    category_email = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[6]/a', 'category_email']
    operator_contains = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/div/div[1]/div/div[3]/span/ul/li[2]/a', 'operator_contains']
    # search_button = [By.CSS_SELECTOR, '#kt_content > div.kt-container.kt-container--fluid.kt-grid__item.kt-grid__item--fluid > div > div > div > div.kt-portlet__body > div:nth-child(1) > div > div > div > div > div > div > div.form-group > button', 'search_button']
    search_button = [By.XPATH, '//button[@class="ml-2 btn btn-wide btn-primary btn-upper"]', 'search_button']
    bulkAction_button = [By.XPATH, '//*[@id="kt_content"]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/button', 'bulkAction_button']
    li_verification = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[1]', "li_verification"]
    li_unverification = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[2]', "li_unverification"]
    li_lock = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[3]', "li_lock"]
    li_unlock = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[4]', "li_unlock"]
    li_delete = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[5]', "li_delete"]
    li_cancelDelete = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[1]', 'li_cancelDelete']
    li_permDelete = [By.XPATH, '//ul[@class="ant-dropdown-menu ant-dropdown-menu-light ant-dropdown-menu-root ant-dropdown-menu-vertical"]/li[2]', 'li_permDelete']
    comment_textarea = [By.XPATH, '//textarea[@id="comment"]', 'comment_textarea']
    comment_phrase_textarea = [By.XPATH, '//input[@id="phrase"]', 'comment_phrase_textarea']
    modal_ok_button = [By.XPATH, '//button[@class="ant-btn ant-btn-primary"]', 'modal_ok_button']
    ext1_modal_ok_button = [By.XPATH, '(//button[@class="ant-btn ant-btn-primary"])[1]', 'ext1_modal_ok_button']
    ext2_modal_ok_button = [By.XPATH, '(//button[@class="ant-btn ant-btn-primary"])[2]', 'ext2_modal_ok_button']

    # TODO due to ongoing Admin Dash work in dev env, different locators are used for same element, will need to update once AD work is complete
    if confTest.globalVar.env == 'dev':
        searchedUser_checkbox = [By.XPATH, '(//input[@type="checkbox"])[2]', 'searchedUser_checkbox']
    else:
        searchedUser_checkbox = [By.XPATH, '//*[@id="local_data"]/div/div/div/div/div/div/table/tbody/tr/td[1]/label/span/input', 'searchedUser_checkbox']
        # searchedUser_checkbox = [By.XPATH, '//*[@id="local_data"]/div/div/div/div/div/div/table/tbody/tr/td[1]/label/span/input']
    pendingDeleteUser_checkbox = [By.XPATH, '(//input[@type="checkbox"])[1]', 'pendingDeleteUser_checkbox']
    no_data_msg = [By.XPATH, '//*[@id="local_data"]/div/div/div/div/div/div/table/tbody/tr/td/div/p', 'no_data_msg']
    extend_button = [By.XPATH, '//button[@class="ant-btn ant-btn-primary"]', 'extend_button']
###==============================================================###
# NYL Services API
###==============================================================###
# [Documentation - Summary] This file creates the variables for
# NYL Services Api testing

# Credentials for NYL Services API
class CREDSapi:
    # obtain creds file from the 1Password QA vault (contact QA lead on project for access)
    # opens specific local creds file with user data according to confTest variable
    if confTest.NYLservicesBASE.testdata == 'iddw':
        notepadfile = open('/Users/Shared/testing/andrewpii.txt', 'r')
    elif confTest.NYLservicesBASE.testdata == 'real':
        notepadfile = open('/Users/Shared/testing/nyl08022021.txt', 'r')
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

###==============================================================###
# NYL SSO
###==============================================================###
# [Documentation - Summary] This section creates the variables for
# NYL Single Sign On page objects for testing user flows

# [Documentation - Variables] Objects on Registration page
# Credentials for SSO Web user
class credsSSOWEB:
    # obtain creds file from the 1Password QA vault (contact QA lead on project for access)
    # opens specific local creds file with user data according to confTest variable
    if confTest.NYlottoBASE.testdata == 'iddw':
        notepadfile = open('/Users/Shared/testing/andrewpii.txt', 'r')
    elif confTest.NYlottoBASE.testdata == 'real':
        notepadfile = open('/Users/Shared/testing/nyl08022021.txt', 'r')
    # turns variable into a list of every line in above notepadfile
    entry_info = notepadfile.read().splitlines()
    fname = funct.getCredential(entry_info, 'sso-first-name')
    lname= funct.getCredential(entry_info, 'sso-last-name')
    housenum = funct.getCredential(entry_info, 'sso-house-number')
    street = funct.getCredential(entry_info, 'sso-street-address')
    city = funct.getCredential(entry_info, 'sso-city')
    state = funct.getCredential(entry_info, 'sso-state')
    zip = funct.getCredential(entry_info, 'sso-zip')
    phone = funct.getCredential(entry_info, 'sso-phone')
    ssn4 = funct.getCredential(entry_info, 'sso-ssn')
    dob_month = funct.getCredential(entry_info, 'sso-dob-month')
    dob_date = funct.getCredential(entry_info, 'sso-dob-date')
    dob_year = funct.getCredential(entry_info, 'sso-dob-year')
    password = funct.getCredential(entry_info, 'sso-test-password')

# Reg page elements
class regV:
    fname = [By.NAME, "firstName", "fname"]
    mname = [By.NAME, "middleName", "mname"]
    lname = [By.NAME, "lastName", "lname"]
    suffix_dropdown = [By.NAME, "suffix", "suffix_dropdown"]
    housenum = [By.NAME, "streetNumber", "housenum"]
    street = [By.NAME, "street", "street"]
    add2 = [By.NAME, "addressLine2", "add2"]
    city = [By.NAME, "city", "city"]
    state_dropdown = [By.NAME, "state", "state_dropdown"]
    zip = [By.NAME, "zip", "zip"]
    phone = [By.NAME, "phone", "phone"]
    ssn4 = [By.NAME, "ssn4", "ssn4"]
    ss_check = [By.NAME, "noSsn4", "ss_check"]
    dob = [By.NAME, "birthdate", "dob"]
    dob_check = [By.NAME, "isOver18", "dob_check"]
    email = [By.ID, "sso-email", "email"]
    password = [By.NAME, "password", "password"]
    confirmPsw = [By.NAME, "confirmPassword", "confirmPsw"]
    tos_check = [By.NAME, "acceptedTermsAndConditions", "tos_check"]
    cnw_check = [By.NAME, "collectnwin", "cnw_check"]
    nylnews_check = [By.NAME, "newsletter", "nylnews_check"]
    submit_button = [By.XPATH, '//*[@id="app-container"]/div/div[2]/div/div/form/div[2]/div[7]/button/span', "submit_button"]

# error variables
    fname_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(2) > div.is-error.invalid-feedback", "fname_error"]
    lname_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(4) > div.is-error.invalid-feedback", "lname_error"]
    housenum_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(6) > div.is-error.invalid-feedback", "housenum_error"]
    street_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(7) > div.is-error.invalid-feedback", "street_error"]
    city_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(9) > div.is-error.invalid-feedback", "city_error"]
    state_dropdown_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > div", "state_dropdown_error"]
    zip_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(11) > div.is-error.invalid-feedback", "zip_error"]
    phone_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.has-prepend > div.is-error.invalid-feedback", "phone_error"]
    dob_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(15) > div.is-error.invalid-feedback", "dob_error"]
    dob_check_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(16) > div > label", "dob_check_error"]
    email_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.form-group.has-prepend > div.is-error.invalid-feedback", "email_error"]
    password_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(3) > div.is-error.invalid-feedback", "password_error"]
    confirmPsw_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(4) > div.is-error.invalid-feedback", "confirmPsw_error"]
    tos_check_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div:nth-child(5) > div > label", "tos_check_error"]
    submit_button_error = [By.XPATH, '//p[@class="submit-error"]', "submit_button_error"]

# error copy
    requiredErrorStub = 'Required'
    submitErrorStub = 'Please see required fields above to complete registration.'
    zipErrorStub = 'Invalid zipcode'
    phoneErrorStub = 'Invalid phone number'
    dobErrorStub = 'Please enter a valid birth date'
    dobErrorUnderageStub = 'You must be 18 years or older to register'
    emailErrorStub = 'Invalid email address'
    passwordErrorStub = 'Your password must follow the password guidelines.'
    confirmPswErrorStub = 'Passwords must match'
    duplicateEmailErrorStub = 'This email is already registered with an account. Please log in or reset your password.'
    duplicatePhoneErrorStub = 'This phone number is already registered with an account. Please log in or reset your password.'

# [Documentation - Variables] Objects on OTP pages
class otpV:
# otp method selection page
    text_button = [By.XPATH, '//*[@id="app-container"]/div/div[2]/div/div/div/button[1]/span']
    call_button = [By.XPATH, '//*[@id="app-container"]/div/div[2]/div/div/div/button[2]/span']
# otp code entry page
    otp_input = [By.NAME, "otp"]
    otp_continue_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(4) > button > span"]
    retry_call_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(5] > p > button:nth-child(1]"]
    retry_text_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(5] > p > button:nth-child(2]"]

# [Documentation - Variables] Objects on Gov ID pages
class govIdV:
# gov id and upload method selection page
    gov_id_dropdown = [By.NAME, "govIdType"]
    id_drivers_license = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.form-group > div > select > option:nth-child(2)"]
    id_passport = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.form-group > div > select > option:nth-child(3)"]
    mobile_button = [By.CLASS_NAME, "nyl-btn"]
    browser_link = [By.CLASS_NAME, "continue-with-browser-link"]

# Drivers license and browser capture method
# Document capture page
    dl_start_button = [By.XPATH, '//button[@id="dcui-start-button"]']
# Driver's license front capture page
    dl_front_capture_button = [By.XPATH, '//button[@id="start-capture"]']
# Driver's license front quality check page
    dl_front_discard_button = [By.XPATH, '//button[@id="discard-capture"]']
    dl_front_save_button = [By.XPATH, '//button[@id="save-capture"]']
# Driver's license back capture page
    dl_back_capture_button = [By.XPATH, '//button[@id="start-capture"]']
# Driver's license back quality check page
    dl_back_discard_button = [By.XPATH, '//button[@id=["discard-capture"]']
    dl_back_save_button = [By.XPATH, '//button[@id="save-capture"]']
# Facial snapshot capture page
    dl_facial_capture_button = [By.XPATH, '//button[@id="start-capture"]']
# Facial snapshot quality check page
    dl_facial_discard_button = [By.XPATH, '//button[@id=["discard-capture"]']
    dl_facial_save_button = [By.XPATH, '//button[@id="save-capture"]']
# Document submission page
    dl_submit_button = [By.XPATH, '//button[@id="verify-all"]']

# Passport and browser capture method
# Document capture page
    passport_start_button = [By.ID, "dcui-start-button"]
# Passport front capture page
    passport_capture_button = [By.ID, "capture-input"]
# Passport front quality check page
    passport_discard_button = [By.ID, "discard-capture"]
    passport_save_button = [By.ID, "save-capture"]
# Facial snapshot capture page
    passport_facial_capture_button = [By.ID, "capture-input"]
# Facial snapshot quality check page
    passport_facial_discard_button = [By.CSS_SELECTOR, "#discard-capture"]
    passport_facial_save_button = [By.CSS_SELECTOR, "#save-capture"]
# Document submission page
    passport_submit_button = [By.ID, "verify-all"]

# TODO at a future date with Appium inspection session
# Drivers license and mobile capture method
# Passport and mobile capture method

# [Documentation - Variables] Objects on Login page
class loginV:
    email = [By.ID, "sso-email", "email"]
    password = [By.NAME, "password", "password"]
    login_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > button > span", "login_button"]
    forgot_password_link = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > p > a", "forgot_password_link"]

# error variables
    email_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.form-group.has-prepend > div.is-error.invalid-feedback", "email_error"]
    password_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(3) > div.is-error.invalid-feedback", "password_error"]
    login_button_error = [By.XPATH, '//p[@class="submit-error"]', "login_button_error"]

# error copy
    requiredErrorStub = 'Required'
    emailErrorStub = 'Invalid email address'
    loginErrorStub = 'There is a problem with the data you entered, please try again.'
    badEmailErrorStub = 'Your email address and password do not match.'
    badPasswordErrorStub = 'Your email address and password do not match.'

# [Documentation - Variables] Objects on Reset Password page
class resetPswV:
    email = [By.NAME, "email"]
    reset_submit_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > button > span"]

# [Documentation - Variables] Objects on Update Profile page
class updateProfV:
    fname = [By.NAME, 'firstName', 'fname']
    mname = [By.NAME, 'middleName', 'mname']
    lname = [By.NAME, 'lastName', 'lname']
    suffix = [By.NAME, 'suffix', 'suffix']
    housenum = [By.NAME, 'streetNumber', 'housenum']
    street = [By.NAME, 'street', 'street']
    add2 = [By.NAME, 'addressLine2', 'add2']
    city = [By.NAME, 'city', 'city']
    state_dropdown = [By.NAME, 'state', 'state_dropdown']
    zip = [By.NAME, 'zip', 'zip']
    phone = [By.NAME, 'phone', 'phone']
    dob = [By.NAME, 'birthdate', 'birthdate']
    email = [By.ID, 'sso-email', 'email']
    update_button = [By.CLASS_NAME, 'nyl-btn', 'update_button']
    signout_button = [By.CLASS_NAME, 'sign-out-all-cta', 'signout_button']

# error variables
    fname_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(2) > div.is-error.invalid-feedback', 'fname_error']
    lname_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(4) > div.is-error.invalid-feedback', 'lname_error']
    housenum_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(6) > div.is-error.invalid-feedback', 'housenum_error']
    street_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(7) > div.is-error.invalid-feedback', 'street_error']
    city_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(9) > div.is-error.invalid-feedback', 'city_error']
    state_dropdown_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.error > div > div', 'state_dropdown_error']
    zip_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(11) > div.is-error.invalid-feedback', 'zip_error']
    phone_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div.form-group.has-prepend > div.is-error.invalid-feedback', 'phone_error']
    dob_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(1) > div:nth-child(13) > div.is-error.invalid-feedback', 'dob_error']
    update_button_error = [By.CSS_SELECTOR, '#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.button-group-wrapper > div > p', 'update_button_error']

# error copy
    requiredErrorStub = 'Required'
    fnameErrorStub = 'Must contain only letters'
    lnameErrorStub = 'Must contain only letters'
    cityLengthErrorStub = 'If your town name is over 21 characters, please submit only 20 characters and the form will identify town based on zip code.'
    zipErrorStub = 'Invalid zipcode'
    phoneErrorStub = 'Invalid phone number'
    dobErrorStub = 'Please enter a valid birth date'
    updateErrorStub = 'All inputs must be valid in order to submit the form.'
