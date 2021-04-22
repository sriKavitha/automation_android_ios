from selenium import webdriver  # webdriver module provides all WebDriver implementations
from selenium.webdriver.common.by import By
import warnings
import unittest, time, re
import requests
import csv
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL
import urllib3
import HtmlTestRunner
import var, funct, confTest     # Custom class

class Rewild(confTest.RewildBrowserBASE):

    def test_brokenImage(self):
        driver = self.driver
        test_urls = []
        with open('sitelinks - TEST.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                test_urls.append(row[0])
                line_count += 1
            print(f'Processed {line_count} lines in CSV file.')

        for t in test_urls:
            driver.get(t)
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight+100));")
            time.sleep(5)
            image_list = driver.find_elements(By.TAG_NAME, "img")
            print('Total number of images on ' + t + ' are ' + str(len(image_list)))
            iBrokenImageCount = 0
            for img in image_list:
                try:
                    response = requests.get(img.get_attribute('src'), stream=True)
                    # print(img.get_attribute('src'))
                    if (response.status_code != 200):
                        print(img.get_attribute('src') + " is broken.")
                        iBrokenImageCount = (iBrokenImageCount + 1)
                except requests.exceptions.MissingSchema:
                    print("Encountered MissingSchema Exception")
                except requests.exceptions.InvalidSchema:
                    print("Encountered InvalidSchema Exception")
                except requests.exceptions.InvalidURL:
                    print("Encountered InvalidURL Exception")
                except:
                    print("Encountered Some other Exception")

            if iBrokenImageCount == 0:
                print('No broken images found.\n')
            else:
                print('ERROR - The page ' + t + ' has ' + str(iBrokenImageCount) + ' broken images\n')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.RewildBrowserBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.RewildBrowserBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))

# # Strategy:
# # navigate to each page (can use sitemap.xml or csv file of links)
# import re
#
# f = open('sitemap.xml','r')
# res = f.readlines()
# for d in res:
#     data = re.findall('<loc>(http:\/\/.+)<\/loc>',d)
#     for i in data:
#         print i
# # search page for img
# # test 1 (cdn change check): grab img src, send httprequest, check status code == 200
# # test 2 (visual check): check height > 10px


