# [Documentation - Setup] This section lists all dependencies
# that are imported for variable file to work
from selenium.webdriver.common.by import By
import funct, confTest

# [Documentation - Summary] This file creates the variables for
# NYL Single Sign On page objects for testing user flows

# [Documentation - Variables] Objects on Registration page
# Credentials for SSO Web user
class credsSSOWEB:
    # obtain creds file from the 1Password QA vault (contact QA lead on project for access)
    # opens specific local creds file with user data according to confTest variable
    if confTest.NYlottoBASE.testdata == 'iddw':
        notepadfile = open('/Users/Shared/testing/andrewpii.txt', 'r')
    elif confTest.NYlottoBASE.testdata == 'real':
        notepadfile = open('/Users/Shared/testing/api01122021.txt', 'r')
    # turns variable into a list of every line in above notepadfile
    entry_info = notepadfile.read().splitlines()
    fname = funct.getCredential(entry_info, 'first-name')
    lname= funct.getCredential(entry_info, 'last-name')
    housenum = funct.getCredential(entry_info, 'house-number')
    street = funct.getCredential(entry_info, 'street-address')
    city = funct.getCredential(entry_info, 'city')
    state = funct.getCredential(entry_info, 'state')
    zip = funct.getCredential(entry_info, 'zip')
    phone = funct.getCredential(entry_info, 'Phone-number')
    ssn4 = funct.getCredential(entry_info, 'ssn')
    dob_month = funct.getCredential(entry_info, 'dob-month')
    dob_date = funct.getCredential(entry_info, 'dob-date')
    dob_year = funct.getCredential(entry_info, 'dob-year')
    password = funct.getCredential(entry_info, 'password')

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
    submit_button = [By.CLASS_NAME, "nyl-btn", "submit_button"]

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
    submit_button_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div:nth-child(2) > div.button-wrap > p", "submit_button_error"]

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
    text_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > div > button.nyl-btn-single.button-1 > span"]
    call_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > div > button.nyl-btn-single.button-2 > span"]
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
    dl_start_button = [By.ID, "dcui-start-button"]
# Driver's license front capture page
    dl_front_capture_button = [By.ID, "capture-input"]
# Driver's license front quality check page
    dl_front_discard_button = [By.ID, "discard-capture"]
    dl_front_save_button = [By.ID, "save-capture"]
# Driver's license back capture page
    dl_back_capture_button = [By.ID, "capture-input"]
# Driver's license back quality check page
    dl_back_discard_button = [By.ID, "discard-capture"]
    dl_back_save_button = [By.ID, "save-capture"]
# Facial snapshot capture page
    dl_facial_capture_button = [By.ID, "capture-input"]
# Facial snapshot quality check page
    dl_facial_discard_button = [By.CSS_SELECTOR, "#discard-capture"]
    dl_facial_save_button = [By.CSS_SELECTOR, "#save-capture"]
# Document submission page
    dl_submit_button = [By.ID, "verify-all"]

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

# May be completed at a future date with Appium inspection session
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
    login_button_error = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > p.submit-error", "login_button_error"]

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