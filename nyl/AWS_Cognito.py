import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import var, funct, util, confTest, HtmlTestRunner  # Custom class for NYL

class NYlotto(confTest.NYlottoBASE):

    def test_01_AWSCognito(self):
        """
        Register the SSO web user. As part of post-registration verification, validate user data in AWS Cognito
        is same as user registration info and LexID is generated in AWS Services(Cognito)
        Purge the SSO user after the verification.
        Dev/QA/Stage/Prod env:
        1. User has to be successfully registered (pre-requisite)
        2. Signin into AWS with valid QA user credentials
        3. Search and select Cognito
        4. Verify the page header - Amazon Cognito
        5. Key in the user pool name and select the pool name
        6. Click the listbox to select the Email address as option from the list
        7. Keyin the email address to search
        8. Click the username link to verify details
        9. Click on Edit button to view more details
        10. Verify the firstname, lastname, address, DOB, phone#, email and LexID in Users page
            a. firstname
            b. lastname
            c. address
            d. DOB
            e. phone
            f. email
            g. LexID/GovID
        https://rosedigital.atlassian.net/browse/MRMNYL-388 (as part of new LexId changes)
        """

        # 1. User has to be successfully registered (pre-requisite)
        driver = self.driver
        # email, testenv = funct.sso_register_customEmail(self)
        email = "testa+sso@rosedigital.co"
        testenv = "qa"
        print('\nUser is now successfully registered....')
        print('----------')

        # 2. Signin into AWS with valid QA user credentials
        driver = self.driver
        # call aws login functionality
        funct.aws_login(self)
        try:
            # Wait for AWS logo to appear after user sign in to AWS
            funct.waitUntil(driver, var.cloudWatchAWS.aws_Logo)
            print('PASS - User is in AWS Home page')
            print('----------')

            # 3. Search and select Cognito from Services
            print('Click on \'Services\' in AWS homepage')
            funct.waitAndClick(driver, var.cloudWatchAWS.aws_services)
            # print('In the search textbox, type \'Cognito\'')
            funct.waitAndSend(driver, var.cloudWatchAWS.aws_services_search, "cognito")
            # print('Click \'Cognito\' under Services option')
            funct.waitAndClick(driver, var.cognitoAWS.aws_cognito_search);

            # 4. Verify the page header - Amazon Cognito
            time.sleep(2)
            funct.waitAndFind(driver, var.cognitoAWS.aws_cognito_cognitoPageHeader)
            print('PASS - Amazon Cognito Page header is verified... ')

            # 5. Key in the user pool name and select the pool name
            print('Key in the user pool name')
            time.sleep(2)
            funct.waitAndSend(driver, var.cognitoAWS.aws_cognito_userPools, "qa-nyl-sso-pool")
            funct.waitAndClick(driver, var.cognitoAWS.aws_cognito_userPoolName)
            driver.execute_script("window.scrollTo(0,250);")

            # 6. Click the listbox to select the Email address as option from the list
            funct.waitAndSend(driver, var.cognitoAWS.aws_cognito_userNamelistBox, "Email address")
            funct.waitAndSend(driver, var.cognitoAWS.aws_cognito_userNamelistBox, Keys.RETURN)

            # 7. Keyin the email address to search
            funct.waitAndClick(driver, var.cognitoAWS.aws_cognito_searchUserAttribute)
            funct.waitAndSend(driver, var.cognitoAWS.aws_cognito_searchUserAttribute, email)
            print("Checking in our database for the email.....: ", email)
            # Check for the matching users with this email address
            count = driver.find_elements_by_xpath("//*[contains(text(),\'No users found\')]")
            if len(count) == 1:
                # Display the message "No users found" on the console
                print("Nope... We are sorry!!! We haven't found any users with this email address..: ", email)
            else:
                print("We found an user with this email... ", email)
                # e_mail = funct.waitAndGetText(driver, var.cognitoAWS.aws_cognito_verifyEmail)

                # 8. Click the username link to verify details
                print("Click the username link to verify details...")
                funct.waitAndClick(driver, var.cognitoAWS.aws_cognito_clickUserNameDetails)
                time.sleep(3)

                # 9. Click on Edit button to view more details
                funct.waitAndClick(driver,var.cognitoAWS.aws_cognito_editButton);

                # Verify the user details
                self.verify_details(email);
        except Exception as e:
            print('Error occurred...', e)
            funct.fullshot(self)
            funct.closeWindow(driver, 'Sign in as IAM user')
        # print("Purging the SSO registered user in Admin Dashboard... by phone number and Email address")
        # funct.purgeSSOemail(self, email)
        # funct.purgeSSOphone(self, var.credsSSOWEB.phone)


    # 10. Verify the firstname, lastname, address, DOB, phone#, email and LexID/GovID
    def verify_details(self, email):
        # a. Verify firstname => SSO web - First name with AWS cognito - First name
        time.sleep(1)
        firstName = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_firstName)

        if (var.credsSSOWEB.fname).capitalize() == firstName.capitalize():
            print('PASS: First Name is successfully verified and is matching with registered firstname...')
        else:
            print('FAIL: First Name in AWS cognito is NOT matching with registered firstname...')
            print(f'\tErr.. First name should be \'{var.credsSSOWEB.fname}\' while it is \'{firstName}\'')
        # print(f"Unverified user account {email} successfully created.")

        # b. Verify lastname => SSO web - Last name with AWS cognito - Last name
        lastName = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_lastName)
        if var.credsSSOWEB.lname == lastName.capitalize():
            print('PASS: Last Name in AWS cognito is successfully verified and is matching with registered lastname...')
        else:
            print('FAIL: Last Name in AWS cognito is NOT matching with registered lastname...')
            print(f'\tErr.. Last name should be \'{var.credsSSOWEB.lname}\' while it is \'{lastName.capitalize()}\'')

        # c. Verify Address => SSO web - address with AWS cognito - Address
        address_ssoweb = var.credsSSOWEB.housenum + ' ' + var.credsSSOWEB.street + ' ' + var.credsSSOWEB.city + ', ' + var.credsSSOWEB.state + ' ' + var.credsSSOWEB.zip
        address_aws = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_address)
        if address_ssoweb.lower()[:10] == address_aws.lower()[0:10]:
            print('PASS: Address in AWS cognito is successfully verified and is matching with registered address...')
        else:
            print('FAIL: Address in AWS cognito is NOT matching with registered address...')
            print(f'\tErr.. Address should be \'{address_ssoweb.lower()}\' while it is \'{address_aws.lower()}\'')

        # d. Verify DOB => SSO web - DOB with AWS cognito - DOB
        dob_aws = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_birthdate)
        dob_sso = str(var.credsSSOWEB.dob_month) + "/" + str(var.credsSSOWEB.dob_date) + "/" + str(var.credsSSOWEB.dob_year)
        if dob_sso == dob_aws:
            print('PASS: DOB in AWS cognito is successfully verified and is matching with registered DOB...')
        else:
            print('FAIL: DOB in AWS cognito is NOT matching with registered DOB ...')
            print(f'\tErr.. DOB should be \'{dob_sso}\' while it is \'{dob_aws}\'')

        # e. Verify phone number => SSO web - phone number with AWS cognito - phone number
        phoneNum = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_phoneNumber)
        phoneWithNumberOne = "+1" + str(var.credsSSOWEB.phone)
        if phoneWithNumberOne == phoneNum:
            print('PASS: Phone# in AWS cognito is successfully verified and is matching with registered Phone#...')
        else:
            print('FAIL: Phone# in AWS cognito is NOT matching with registered Phone# ...')
            print(f'\tErr.. Phone# should be \'{phoneWithNumberOne}\' while it is \'{phoneNum}\'')

        # f. Verify email address => SSO web - email with AWS cognito - email
        if email == funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_email):
            print('PASS: eMail in AWS cognito is successfully verified and is matching with registered eMail address...')
        else:
            print('FAIL: eMail in AWS cognito is NOT matching with registered eMail address...')
            print(f'\tErr.. Email should be \'{email}\' while it is \'{var.cognitoAWS.aws_cognito_email}\'')

        # g. Verify LexId/GovId is generated
        if len(self.driver.find_elements_by_xpath('//div[@data-testid="optional-attribute-custom:lex_id"]//input')) == 1:
            id = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_lexIDNumber)
            print("PASS: Lex ID is successfully generated:", id)
        elif len(self.driver.find_elements_by_xpath('//div[@data-testid="optional-attribute-custom:gov_id"]//input')) == 1:
            id = funct.waitAndGetAttributeValue(self.driver, var.cognitoAWS.aws_cognito_govIDNumber)
            print("PASS: Gov ID is successfully generated: ", id)
        else:
            print("FAIL: Either LexID or GovID is not generated for this user...", email)
            raise Exception("\tPlease contact the customer rep to fix your account")

        print('\n ---------Registered \'SSO web user\' details are verified against \'AWS Cognito\'-----')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))
