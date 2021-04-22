from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re
import requests, json           # Requests provides ability to hit API Json provides ability to encode & decode Json files
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL
import csv
import HtmlTestRunner
import var, funct, confTest     # Custom class

class Rewild(confTest.RewildBrowserBASE):
    # check redirects by opening browser, waiting for redirect, verifying the url is as expected
    def test_redirectsTest(self):
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
            try:
                r = requests.get(f, allow_redirects=True)
                l = r.headers.get('location')
                redirectLocation = str(l)
                if redirectLocation == t:
                    redirectsPassedList.append(f)
                    print('Successful redirect on: ' + f + ' Returned url: ' + redirectLocation)
                else:
                    redirectsFailedUrls.append(f)
                    redirectsExpectedUrls.append(t)
                    redirectsCurrentUrls.append(l)
                    print(r.status_code)
                    print('Failed redirect: ' + f + ' Expected url: ' + t + ' Returned url: ' + redirectLocation)

            except requests.exceptions.MissingSchema:
                print("Encountered MissingSchema Exception")
            except requests.exceptions.InvalidSchema:
                print("Encountered InvalidSchema Exception")
            except requests.exceptions.InvalidURL:
                print("Encountered InvalidURL Exception")
            except:
                print("Encountered Some other Exception")

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.RewildBrowserBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.RewildBrowserBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))