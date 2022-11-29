import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases

from selenium.webdriver.common.keys import Keys

import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL
import AWS_login_success

class NYlotto(confTest.NYawsBASE):


    def test_01_AWSCloudWatch(self):
        """
        Verify the logs in AWS(cloudwatch) after a SSO user is successfully registered in
        Dev/QA/Stage/Prod env:
        1. User has to be successfully registered (prerequsite)
        2. Signin into AWS with QA user credentials
        3. Search and select CloudWatch from Services
        4. Click Logs > Log Groups
        5. Filter and Select the appropriate log groups based on environment
        6. Click the Log event based on the log event time and filter the activity
        7. Check for success status

        https://rosedigital.atlassian.net/browse/MRMNYL-369
        https://rosedigital.atlassian.net/browse/MRMNYL-370 (Manual testcase for MRMNYL-369)

        """
        # 1. User has to be successfully registered (prerequsite)
        print('\nRegistering a SSO user...')
        # Get the local time and convert into timestamp: %Y-%m-%d %H:%M:%S format
        ts = time.localtime()
        timeUserCreated = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        # Register the user with the email format: qa+sso+timeUserCreated+@rosedigital.co
        email = 'qa+sso' + str(timeUserCreated) + '@rosedigital.co'
        # creates a verified user with valid SSN4
        funct.createVerifiedUser(self, email)
        print('\nUser is successfully registered....')
        # Get the timestamp only from the email to compare with log event time
        userName = email.split('@')
        time_userCreated = userName[0][6:]
        print('----------')
        # 2. Signin into AWS with QA user credentials
        driver = self.driver
        # call aws login functionality
        funct.aws_login(self)
        try:
            # Check if user is successfully signed in to aws...
            if driver.find_element_by_id("nav-home-link") != []:
                print('PASS - AWS login successful and redirected to AWS homepage uri')
                print('----------')

                # 3.Search and select CloudWatch from Services
                print('Click on \'Services\' in AWS homepage')
                funct.waitAndClick(driver, var.cloudWatchAWS.aws_services)
                print('In the search textbox, type \'CloudWatch\'')
                funct.waitAndSend(driver, var.cloudWatchAWS.aws_services_search, "cloudwatch")
                print('Click \'CloudWatch\' under Services option')
                funct.waitAndClick(driver, var.cloudWatchAWS.aws_cloudwatch_search);

                # 4. Click Logs > Log Groups
                print('Click on \'Logs\' in Cloud Watch page')
                funct.waitAndClick(driver, var.cloudWatchAWS.aws_logs)
                print('Navigate to \'Log Groups\' page upon clicking on \'Log groups\' link')
                funct.waitAndClick(driver, var.cloudWatchAWS.aws_logGroups)

                # 5. Filter and Select the appropriate log groups based on environment
                driver.switch_to.frame('microConsole-Logs')
                time.sleep(5)
                print('Keyin \'qa-postssoregisterverify\' in filter log groups textbox to search the required log groups')
                funct.waitAndSend(driver, var.cloudWatchAWS.aws_logGroupsSearch, 'qa-postssoregisterverify')
                print('Click the \'qa-postssoregisterverify\' group name')
                funct.waitAndClick(driver, var.cloudWatchAWS.aws_logGroupsSearchResults)

                # 6. Click the Log event based on the log event time and filter the activity
                """Compare qa+sso email-registartion created timestamp with the first log event time
                before clicking the log stream"""
                time.sleep(2)
                eventTime = driver.find_element_by_xpath('//table[@role=\'table\']//tr[1]/td[3]').text
                if str(time_userCreated) == str(eventTime[:19]):
                    print('Click \'Log Stream\' to view logs for the Registered Email...')
                    funct.waitAndClick(driver, var.cloudWatchAWS.aws_logStream)
                    print('key in \"nyl-services-qa-postSsoRegisterVerify-SendResponse\" in the textbox and press Enter key to search')
                    funct.waitAndSend(driver, var.cloudWatchAWS.aws_logEventsSearch, '"nyl-services-qa-postSsoRegisterVerify-SendResponse"')
                    funct.waitAndSend(driver, var.cloudWatchAWS.aws_logEventsSearch, Keys.RETURN)
                    funct.waitAndClick(driver, var.cloudWatchAWS.aws_openAll)

                    # 7. Check for success label, status code as 200, status as SUCCESS
                    try:
                        funct.waitAndFind(driver, var.cloudWatchAWS.aws_logStatusCode_successLabel)
                        funct.waitAndFind(driver, var.cloudWatchAWS.aws_logStatusCode_successCode)
                        funct.waitAndFind(driver, var.cloudWatchAWS.aws_logStatus_SUCCESS)
                        print('----------')
                        print('AWS CloudWatch logs are successfully verified...')
                    except Exception as e:
                        print("Exception error...",e)

                    funct.closeWindow(driver, 'Sign in as IAM user')
                    print('----------')
                else:
                    pass
            else:
                raise Exception('Unexpected behavior encountered')
        except Exception as e:
                print("AWS Login attempt is unsuccessful...", e)
                funct.fullshot(self)
                print('FAIL - AWS Login attempt failed')
                funct.closeWindow(driver, 'Sign in as IAM user')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))