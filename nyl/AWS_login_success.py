import unittest, time, re       #unittest is the testing framework, provides module for organizing test cases
import var, funct, util, confTest, HtmlTestRunner   #Custom class for NYL

class NYlotto(confTest.NYawsBASE):


    def test_01_AWSloginSuccess(self):
        """Checks that a AWS user can login in successfully
        """
        driver = self.driver
        funct.aws_login(self)
        # Successful login should redirect to AWS page
        # Checking AWS logo present on page
        try:
            if driver.find_element_by_id("nav-home-link") != []:
                print('PASS - AWS login successful and redirected to AWS homepage uri')
            else:
                raise Exception('Unexpected behavior encountered')
        except Exception as e:
             funct.fullshot(driver)
             print('FAIL - AWS Login attempt failed', e)
             raise Exception('Unexpected behavior encountered')

        funct.closeWindow(driver, 'Sign in as IAM user')
        print('----------')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYlottoBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYlottoBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))