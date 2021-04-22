from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re
import csv
import HtmlTestRunner
import var, funct, confTest     # Custom class

class Rewild(confTest.RewildBrowserBASE):
    # check redirects by opening browser, waiting for redirect, verifying the url is as expected
    def test_redirects(self):
        driver = self.driver
        from_urls = []
        to_urls = []
        with open('redirect-test.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                from_urls.append(row[0])
                to_urls.append(row[1])
                line_count += 1
            print(f'Processed {line_count} lines in CSV file.')
            # print(from_urls)
            # print(to_urls)

        # from_urls = ['https://rewildstaging.wpengine.com/']
        # to_urls = ['https://www.rewild.org']
        redirectsPassedList = []
        redirectsFailedUrls = []
        redirectsExpectedUrls = []
        redirectsCurrentUrls = []
        redirectsFailedList = []

        for f, t in zip(from_urls, to_urls):
            driver.get('https://www.google.com')
            # open new window with execute_script()
            driver.execute_script("window.open('');")
            # switch to new window with switch_to.window()
            driver.switch_to.window(driver.window_handles[1])
            driver.get(f)
            time.sleep(20)
            if driver.current_url == t:
                redirectsPassedList.append(f)
                print('Successful redirect on: ' + f + ' Returned url: ' + driver.current_url)
            else:
                redirectsFailedUrls.append(f)
                redirectsExpectedUrls.append(t)
                redirectsCurrentUrls.append(driver.current_url)
                print('Failed redirect: ' + f + ' Expected url: ' + t + ' Returned url: ' + driver.current_url)
            driver.close()
            # switch back to old window with switch_to.window()
            driver.switch_to.window(driver.window_handles[0])

        for f, e, c in zip(redirectsFailedUrls, redirectsExpectedUrls, redirectsCurrentUrls):
            redirectsFailedList.append([(f, e, c)])

        if redirectsFailedList != []:
            print("ERROR - These individual urls did NOT redirect as expected:")
            print(f'(Initial URL, Expected URL, Returned URL)')
            print(redirectsFailedList)
        else:
            print("PASS - ALL individual urls redirected as expected ")


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.RewildBrowserBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.RewildBrowserBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))