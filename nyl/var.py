#Single Sign On elements for testing user flows


#elements on Registration page
class regV
    fname = (By.name, "firstName")
    mname = (By.name, "middleName")
    lname = (By.name, "lastName")
    suffix_dropdown = (By.name, "suffix")
    housenum = (By.name, "streetNumber")
    street = (By.name, "street")
    add2 = (By.name, "addressLine2")
    city = (By.name, "city")
    state_dropdown = (By.name, "state")
    zip = (By.name, "zip")
    phone = (By.name, "phone")
    ssn4 = (By.name, "ssn4")
    ss_check = (By.name, "noSsn4")
    dob = (By.name, "birthdate")
    dob_check = (By.name, "isOver18")
    email = (By.id, "sso-email")
    password = (By.name, "password")
    passwordc = (By.name, "confirmPassword")
    tos_check = (By.name, "acceptedTermsAndConditions")
    cnw_check = (By.name, "collectnwin")
    nylnews_check = (By.name, "newsletter")
    submit_button = (By.className, "nyl-btn")

#elements on OTP pages
class otpV
#otp method selection page
    text_button = (By.className, "nyl-btn-single button-1")
    call_button = (By.className, "nyl-btn-single button-2")
#otp code entry page
    otp_input = (By.name, "otp")
    otp_continue_button = (By.cssSelector, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(4) > button > span")
    retry_call_button = (By.cssSelector, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(5) > p > button:nth-child(1)")
    retry_text_button = (By.cssSelector, "#app-container > div > div.container__content > div > div > form > div > div:nth-child(5) > p > button:nth-child(2)")

#elements on Gov ID pages
class govIdV
#gov id and upload method selection page
    gov_id_dropdown = (By.name, "govIdType")
    mobile_button = (By.className, "ny;l-btn")
    browser_link = (By.className, "continue-with-browser-link")
#Drivers license and browser method
    start_button = (By.id, "dcui-start-button")
#start capture screen


#elements on Update Profile page
class upProfV
    fname = (By.name, "firstName")
    mname = (By.name, "middleName")
    lname = (By.name, "lastName")
    suffix = (By.name, "suffix")
    housenum = (By.name, "streetNumber")
    street = (By.name, "street")
    add2 = (By.name, "addressLine2")
    city = (By.name, "city")
    state = (By.name, "state")
    zip = (By.name, "zip")
    phone = (By.name, "phone")
    dob = (By.name, "birthdate")
    email = (By.id, "sso-email")
    updateSubmitBtn = (By.className, "nyl-btn")
