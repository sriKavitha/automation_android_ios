# [Documentation - Setup] This section lists all dependencies
# that are imported for variable file to work
from selenium.webdriver.common.by import By

# [Documentation - Summary] This file creates the variables for
# NYL Single Sign On page objects for testing user flows

# [Documentation - Variables] Objects on Registration page
class regV:
    fname = [By.NAME, "firstName"]
    mname = [By.NAME, "middleName"]
    lname = [By.NAME, "lastName"]
    suffix_dropdown = [By.NAME, "suffix"]
    housenum = [By.NAME, "streetNumber"]
    street = [By.NAME, "street"]
    add2 = [By.NAME, "addressLine2"]
    city = [By.NAME, "city"]
    state_dropdown = [By.NAME, "state"]
    zip = [By.NAME, "zip"]
    phone = [By.NAME, "phone"]
    ssn4 = [By.NAME, "ssn4"]
    ss_check = [By.NAME, "noSsn4"]
    dob = [By.NAME, "birthdate"]
    dob_check = [By.NAME, "isOver18"]
    email = [By.ID, "sso-email"]
    password = [By.NAME, "password"]
    passwordc = [By.NAME, "confirmPassword"]
    tos_check = [By.NAME, "acceptedTermsAndConditions"]
    cnw_check = [By.NAME, "collectnwin"]
    nylnews_check = [By.NAME, "newsletter"]
    submit_button = [By.CLASS_NAME, "nyl-btn"]

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
    dl_facial_capture_button = [By.ID, "start-capture"]
# Facial snapshot quality check page
    dl_facial_discard_button = [By.ID, "discard-capture"]
    dl_facial_save_button = [By.ID, "save-capture"]
# Document submission page
    dl_submit_button = [By.ID, "verify-all"]

# Passport and browser capture method
# Document capture page
    passport_start_button = [By.ID, "dcui-start-button"]
# Passport front capture page
    passport_capture_button = [By.ID, "start-capture"]
# Passport front quality check page
    passport_discard_button = [By.ID, "discard-capture"]
    passport_save_button = [By.ID, "save-capture"]
# Facial snapshot capture page
    passport_facial_capture_button = [By.ID, "start-capture"]
# Facial snapshot quality check page
    passport_facial_discard_button = [By.ID, "discard-capture"]
    passport_facial_save_button = [By.ID, "save-capture"]
# Document submission page
    passport_submit_button = [By.ID, "verify-all"]

# May be completed at a future date with Appium inspection session
# Drivers license and mobile capture method
# Passport and mobile capture method

# [Documentation - Variables] Objects on Login page
class loginV:
    email = [By.ID, "sso-email"]
    password = [By.NAME, "password"]
    login_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > button > span"]
    forgot_password_link = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > p > a"]

# [Documentation - Variables] Objects on Reset Password page
class resetPswV:
    email = [By.NAME, "email"]
    reset_submit_button = [By.CSS_SELECTOR, "#app-container > div > div.container__content > div > div > form > div > div.button-wrap > button > span"]

# [Documentation - Variables] Objects on Update Profile page
class updateProfV:
    fname = [By.NAME, "firstName"]
    mname = [By.NAME, "middleName"]
    lname = [By.NAME, "lastName"]
    suffix = [By.NAME, "suffix"]
    housenum = [By.NAME, "streetNumber"]
    street = [By.NAME, "street"]
    add2 = [By.NAME, "addressLine2"]
    city = [By.NAME, "city"]
    state = [By.NAME, "state"]
    zip = [By.NAME, "zip"]
    phone = [By.NAME, "phone"]
    dob = [By.NAME, "birthdate"]
    email = [By.ID, "sso-email"]
    update_submit_button = [By.CLASS_NAME, "nyl-btn"]
