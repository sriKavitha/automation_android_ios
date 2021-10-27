from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
import requests     # Requests provides ability to hit API
from random import randint
import json
import jwt      # Pyjwt provides ability to encode & decode JSON web tokens
# import HtmlTestRunner

import var, funct, confTest     # Custom class for NYL

class NYLadmin(confTest.NYLadminBASE):

    def test_apiStatusCode(self):
        # [Documentation - Summary] Checks that response status code 200 is returned
        # for Admin Dash API endpoints

        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")

        if self.env == 'dev':
            admin_client_id = '7o78gaj00d672ernobk1pll51p'
        elif self.env == 'qa':
            admin_client_id = '7nankvp2eifim3hfe5t12dtk7v'
        elif self.env == 'stage':
            admin_client_id = '11rgrqr6pb91k0ef237odv5nm6'

        if self.env == 'dev':
            user_pool_id = 'us-east-1_GFTjSQrHQ'
        elif self.env == 'qa':
            user_pool_id = 'us-east-1_QZZDGaPyw'
        elif self.env == 'stage':
            user_pool_id = 'us-east-1_v3S7DZTfs'

        ts = funct.timeStamp()
        # email for admin invite
        testemailAdmin = 'qa+admin@rosedigital.co'

        # time.sleep() added between calls so tests do not hit AWS Batch API limits

        print('\n----------\n' + 'Test setup')
        print('Generating auth token for admin dash')
        # logging into Admin Dash from FE and grabbing auth token for use in API calls
        driver = self.driver
        # url is pulled from confTest
        driver.get(self.admin_url)
        funct.waitAndSend(driver, var.adminLoginVar.email, var.CREDSadmin.superadmin_username)
        funct.waitAndSend(driver, var.adminLoginVar.password, var.CREDSadmin.superadmin_psw)
        funct.waitAndClick(driver, var.adminLoginVar.signin_button)
        if driver.find_elements_by_xpath(var.adminDashVar.home_breadcrumb_link[1]) != []:
            print('PASS - Admin Dash login successful')
        else:
            funct.fullshot(driver)
            print('FAIL - Admin Dash login attempt failed or redirected incorrectly')
            raise Exception('Unexpected behavior encountered')
        cookie_AccessToken = driver.get_cookie('NYL_ADMIN_ACCESS_TOKEN')  # grabs dictionary of the cookie with name = 'NYL_ADMIN_ACCESS_TOKEN'
        cookie_gcl_au = driver.get_cookie('_gcl_au')
        admin_access_token = (cookie_AccessToken['value'])  # assigns the actual token value to the variable
        admin_gcl_cookie = (cookie_gcl_au['value'])
        time.sleep(2)

        print("\ncreating users to manipulate in the admin dash\n")
        # Creating users to manipulate in the admin dash
        # grabbing entry info through localized var/ funct files
        if testenv == 'dev':
            sso_client_id = var.CREDSapi.devSSOcid
        elif testenv == 'qa':
            sso_client_id = var.CREDSapi.qaSSOcid
        elif testenv == 'stage':
            sso_client_id = var.CREDSapi.stageSSOcid

        # Check for existing test SSO user and wipe it from userpool prior to register api call
        # No check done on dev as duplicate phone is disabled for development purposes
        if testenv == 'dev':
            pass
        else:
            try:
                funct.purgeSSOphone(self, var.CREDSapi.ssoPhone)
            except:
                pass

        # Create SSO user via register-verify api call,
        # grab and decrypt cognito sub from JSON response
        # for admin user id api calls further down
        # create users list pairs with email address and cognito sub
        # for api calls further down
        test_user_emails = []
        test_user_subs = []
        i = 0
        num_test_users = 10
        while i < num_test_users:
            ts = funct.timeStamp()
            testemailSSO = 'qa+sso' + ts + '@rosedigital.co'
            sso_register_payload = {'clientId': sso_client_id, 'email': testemailSSO, 'password': var.CREDSapi.ssoPW,
                                    'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                    'phone': var.CREDSapi.ssoPhone,
                                    'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                    'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                    'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState,
                                    'zip': var.CREDSapi.ssoZip, 'ssn4': var.CREDSapi.ssoSSN, 'noSsn4': 'false'}
            sso_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                             json=sso_register_payload)
            # [Documentation - detail] grabbing the idToken from the registration response body
            if '"phoneDuplicate":true' in str(sso_registerCall.text):
                print('ERROR - Duplicate phone for user and user not created.\nRegistration response = ')
                print(f'Response = {sso_registerCall.text}')
                raise Exception(
                    'Failed user creation. Unable to proceed further. Purge phone number or change user data.')
            elif '"hardFail":true' in str(sso_registerCall.text):
                print('ERROR - IDDW Verification failed for user and user not created.\nRegistration response = ')
                print(f'Response = {sso_registerCall.text}')
                raise Exception('Failed user creation. Unable to proceed further. Change test user data in creds file.')
            else:
                registerResponse = []
                quoted = re.compile('"(.*?)"')
                for value in quoted.findall(sso_registerCall.text):
                    registerResponse.append(value)
                try:
                    # grabbing generated user email and cognito sub and adding to user list
                    sso_register_id_token = registerResponse[9]
                    # print(sso_registerCall.text)
                    # print(sso_register_id_token)
                    encoded = sso_register_id_token
                    decoded = jwt.decode(encoded, options={"verify_signature": False})  # decoding the idToken
                    test_user_emails.append(decoded['email'])
                    test_user_subs.append(decoded['sub'])
                    # print(test_user_emails[i])
                    # print(test_user_subs[i])
                    time.sleep(1)
                    # updating the current user phone number to fake randomized number so we can create more users with same test data
                    admin_ssoUsers_headers1 = {'Authorization': admin_access_token}
                    admin_ssoUsers_payload1 = {'comment': 'api automated testing',
                                               "profileUpdate": {'email': testemailSSO,
                                                                 'firstName': var.CREDSapi.ssoFName,
                                                                 'lastName': var.CREDSapi.ssoLName,
                                                                 'phone': '555'+str(randint(2000000, 9999999)),
                                                                 'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                                                 'streetNumber': var.CREDSapi.ssoHNum,
                                                                 'street': var.CREDSapi.ssoStreet,
                                                                 'city': var.CREDSapi.ssoCity,
                                                                 'state': var.CREDSapi.ssoState,
                                                                 'zip': var.CREDSapi.ssoZip}}
                    admin_ssoUsersPatchCall1 = requests.patch(
                        f'https://api-{self.env}.nylservices.net/admin/users/{test_user_subs[i]}',
                        headers=admin_ssoUsers_headers1, json=admin_ssoUsers_payload1)
                    if admin_ssoUsersPatchCall1.status_code == 200:
                        pass
                        # print('update phone successful')
                    else:
                        print(f'could not update phone number in test user {testemailSSO}')
                        print(f"ERROR - PUT /sso/register-verify (Profile Update) Status Code: {admin_ssoUsersPatchCall1.status_code}")
                        print(f'Response headers: {admin_ssoUsersPatchCall1.headers}')
                        print(f'Response: {admin_ssoUsersPatchCall1.text}')
                except:
                    pass
                time.sleep(1)
                i += 1
        print(test_user_emails)
        print(test_user_subs)
        print('Test setup complete' + '\n----------\n\n')


        # GET /admin/login-response
        admin_loginResponse_headers = {"cookie": "_gcl_au="+admin_gcl_cookie}
        admin_loginResponseGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/login-response', headers=admin_loginResponse_headers)
        if admin_loginResponseGetCall.status_code == 200:
            print(f"GET /admin/login-response Status Code: {admin_loginResponseGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/login-response Status Code: {admin_loginResponseGetCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_loginResponseGetCall.headers}\n')
            print(f'RESPONSE: {admin_loginResponseGetCall.text}\n')
        time.sleep(2)

        # GET /admin/admin_users
        admin_adminUsers_headers1 = {'Authorization': admin_access_token}
        admin_adminUsersGetCall1 = requests.get('https://api-' + self.env + '.nylservices.net/admin/admin_users', headers=admin_adminUsers_headers1)
        if admin_adminUsersGetCall1.status_code == 200:
            print(f"GET /admin/admin_users Status Code: {admin_adminUsersGetCall1.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users Status Code: {admin_adminUsersGetCall1.status_code}")
            print(f'RESPONSE HEADERS: {admin_adminUsersGetCall1.headers}\n')
            print(f'RESPONSE: {admin_adminUsersGetCall1.text}\n')
        time.sleep(2)

        # GET /admin/admin_users with params
        admin_adminUsers_params2 = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_adminUsers_headers2 = {'Authorization': admin_access_token}
        admin_adminUsersGetCall2 = requests.get('https://api-' + self.env + '.nylservices.net/admin/admin_users', params=admin_adminUsers_params2, headers=admin_adminUsers_headers2)
        if admin_adminUsersGetCall2.status_code == 200:
            print(f"GET /admin/admin_users with Params Status Code: {admin_adminUsersGetCall2.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users with Params Status Code: {admin_adminUsersGetCall2.status_code}")
            print(f'RESPONSE HEADERS: {admin_adminUsersGetCall2.headers}\n')
            print(f'RESPONSE: {admin_adminUsersGetCall2.text}\n')
        time.sleep(2)

        # GET /admin/admin_users with search terms
        admin_adminUsers_params3 = {"search_term": "e", "limit": 10, "offset": 0, "column": "", "order": ""}
        admin_adminUsers_headers3 = {'Authorization': admin_access_token}
        admin_adminUsersGetCall3 = requests.get('https://api-' + self.env + '.nylservices.net/admin/admin_users', params=admin_adminUsers_params3, headers=admin_adminUsers_headers3)
        if admin_adminUsersGetCall3.status_code == 200:
            print(f"GET /admin/admin_users with Search Term Status Code: {admin_adminUsersGetCall3.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users with Search Term Status Code: {admin_adminUsersGetCall3.status_code}")
            print(f'RESPONSE HEADERS: {admin_adminUsersGetCall3.headers}\n')
            print(f'RESPONSE: {admin_adminUsersGetCall3.text}\n')
        time.sleep(2)

        # POST /admin/invite
        admin_invite_headers = {'Authorization': admin_access_token}
        admin_invite_payload = {"firstName": "QA", "lastName": "Tester", "phone": "3472929732", "email": testemailAdmin, "isSuperadmin": "false"}
        admin_invitePostCall = requests.post('https://api-' + self.env + '.nylservices.net/admin/invite',
                                            headers=admin_invite_headers, json=admin_invite_payload)
        if admin_invitePostCall.status_code == 200:
            print(f"POST /admin/invite Status Code: {admin_invitePostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/invite Status Code: {admin_invitePostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_invitePostCall.headers}\n')
            print(f'RESPONSE: {admin_invitePostCall.text}\n')
        time.sleep(2)

        # PATCH /admin/admin_users/{admin_user_id}
        if self.env == 'dev':
            admin_user_id = '531899f9-9b54-4e6e-a0fc-1b6ec139bd7e'
        elif self.env == 'qa':
            admin_user_id = '70632c6a-f18d-485b-9b81-0837c2361278'
        elif self.env == 'stage':
            admin_user_id = 'a2e9b68a-b7be-48c5-b325-516cb22eb013'

        admin_adminUsersPatch_headers = {'Authorization': admin_access_token}
        admin_adminUsersPatch_payload = {"roleUpdate": {"role": "csr"}, "profileUpdate": {"firstName": "QA", "lastName": "Tester", "phone": "3472929732"}}
        admin_adminUsersPatchCall = requests.patch(f'https://api-{self.env}.nylservices.net/admin/admin_users/{admin_user_id}',
                                            headers=admin_adminUsersPatch_headers, json=admin_adminUsersPatch_payload)
        if admin_adminUsersPatchCall.status_code == 200:
            print(f"PATCH /admin/admin_users/admin_user_id Status Code: {admin_adminUsersPatchCall.status_code}")
        else:
            print(f"ERROR - PATCH /admin/admin_users/admin_user_id Status Code: {admin_adminUsersPatchCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_adminUsersPatchCall.headers}\n')
            print(f'RESPONSE: {admin_adminUsersPatchCall.text}\n')
        time.sleep(2)

        # PUT /admin/admin_users/{admin_user_id}/status
        admin_adminUsersStatus_headers = {'Authorization': admin_access_token}
        admin_adminUsersStatus_payload = {"enabled": "false"}
        admin_adminUsersStatusPutCall = requests.put(
            f'https://api-{self.env}.nylservices.net/admin/admin_users/{admin_user_id}/status',
            headers=admin_adminUsersStatus_headers, json=admin_adminUsersStatus_payload)
        if admin_adminUsersStatusPutCall.status_code == 200:
            print(f"PUT /admin/admin_users/admin_user_id/status Status Code: {admin_adminUsersStatusPutCall.status_code}")
        else:
            print(f"ERROR - PUT /admin/admin_users/admin_user_id/status Status Code: {admin_adminUsersStatusPutCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_adminUsersStatusPutCall.headers}\n')
            print(f'RESPONSE: {admin_adminUsersStatusPutCall.text}\n')
        time.sleep(2)

        # GET /admin/features
        admin_features_headers = {'Authorization': admin_access_token}
        admin_featuresGetCall = requests.get(
            f'https://api-{self.env}.nylservices.net/admin/features',
            headers=admin_features_headers)
        if admin_featuresGetCall.status_code == 200:
            print(f"GET /admin/features Status Code: {admin_featuresGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/features Status Code: {admin_featuresGetCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_featuresGetCall.headers}\n')
            print(f'RESPONSE: {admin_featuresGetCall.text}\n')
        time.sleep(2)

        # PUT /admin/features/ticket-scan
        admin_ticketscan_headers = {'Authorization': admin_access_token}
        admin_ticketscan_payload = {'scanCountLimit': 2000, 'isEnabled': 'true', 'comment': 'api testing', 'isUnlimited': 'false'}
        admin_ticketscanPutCall = requests.put(
            f'https://api-{self.env}.nylservices.net/admin/features/ticket-scan',
            headers=admin_ticketscan_headers, json=admin_ticketscan_payload)
        if admin_ticketscanPutCall.status_code == 200:
            print(f"PUT /admin/features/ticket-scan Status Code: {admin_ticketscanPutCall.status_code}")
        else:
            print(f"ERROR - PUT /admin/features/ticket-scan Status Code: {admin_ticketscanPutCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_ticketscanPutCall.headers}\n')
            print(f'RESPONSE: {admin_ticketscanPutCall.text}\n')
        time.sleep(2)

        # GET /admin/features-audit-log
        admin_featuresAudit_headers1 = {'Authorization': admin_access_token}
        admin_featuresAuditGetCall = requests.get(f'https://api-{self.env}.nylservices.net/admin/features-audit-log', headers=admin_featuresAudit_headers1)
        if admin_featuresAuditGetCall.status_code == 200:
            print(f"GET /admin/features-audit-log Status Code: {admin_featuresAuditGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/features-audit-log Status Code: {admin_featuresAuditGetCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_featuresAuditGetCall.headers}\n')
            print(f'RESPONSE: {admin_featuresAuditGetCall.text}\n')
        time.sleep(2)

        # POST /admin/features-audit-log
        admin_featuresAudit_headers2 = {'Authorization': admin_access_token}
        admin_featuresAudit_payload2 = {'comment': 'automated testing'}
        admin_featuresAuditPostCall = requests.post(f'https://api-{self.env}.nylservices.net/admin/features-audit-log', headers=admin_featuresAudit_headers2, json=admin_featuresAudit_payload2)
        if admin_featuresAuditPostCall.status_code == 200:
            print(f"POST /admin/features-audit-log Status Code: {admin_featuresAuditPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/features-audit-log Status Code: {admin_featuresAuditPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_featuresAuditPostCall.headers}\n')
            print(f'RESPONSE: {admin_featuresAuditPostCall.text}\n')
        time.sleep(2)


        # GET /admin/users
        admin_ssoUsers_headers2 = {'Authorization': admin_access_token}
        admin_ssoUsersGetCall1 = requests.get('https://api-' + self.env + '.nylservices.net/admin/users', headers=admin_ssoUsers_headers2)
        if admin_ssoUsersGetCall1.status_code == 200:
            print(f"GET /admin/users Status Code: {admin_ssoUsersGetCall1.status_code}")
        else:
            print(f"ERROR - GET /admin/users Status Code: {admin_ssoUsersGetCall1.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoUsersGetCall1.headers}\n')
            print(f'RESPONSE: {admin_ssoUsersGetCall1.text}\n')
        time.sleep(2)

        # GET /admin/users with params
        # https://api-dev.nylservices.net/admin/users?limit=10&offset=0&column=&order=
        admin_ssoUsers_params3 = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoUsers_headers3 = {'Authorization': admin_access_token}
        admin_ssoUsersGetCall2 = requests.get('https://api-' + self.env + '.nylservices.net/admin/users', params=admin_ssoUsers_params3, headers=admin_ssoUsers_headers3)
        if admin_ssoUsersGetCall2.status_code == 200:
            print(f"GET /admin/users with params Status Code: {admin_ssoUsersGetCall2.status_code}")
        else:
            print(f"ERROR - GET /admin/users with params Status Code: {admin_ssoUsersGetCall2.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoUsersGetCall2.headers}\n')
            print(f'RESPONSE: {admin_ssoUsersGetCall2.text}\n')
        time.sleep(2)

        # TODO GET /admin/users with search terms
        # search_term (if searching)column, order (if sorting)
        admin_ssoUsers_params4 = {"search_term": test_user_emails[0], "limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoUsers_headers4 = {'Authorization': admin_access_token, "Accept": "application/json", "Content-Type": "application/json", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoUsersGetCall3 = requests.get('https://api-' + self.env + '.nylservices.net/admin/users', params=admin_ssoUsers_params4, headers=admin_ssoUsers_headers4)
        if admin_ssoUsersGetCall3.status_code == 200:
            print(f"GET /admin/users with search terms Status Code: {admin_ssoUsersGetCall3.status_code}")
        else:
            print(f"ERROR - GET /admin/users with search terms Status Code: {admin_ssoUsersGetCall3.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoUsersGetCall3.headers}\n')
            print(f'RESPONSE: {admin_ssoUsersGetCall3.text}\n')
        time.sleep(2)

        # GET /admin/users/{user_id}
        # user_id pulled from test setup sso users
        admin_ssoUsers_headers5 = {'Authorization': admin_access_token}
        admin_ssoUsersGetCall4 = requests.get(f'https://api-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}', headers=admin_ssoUsers_headers5)
        if admin_ssoUsersGetCall4.status_code == 200:
            print(f"GET /admin/users/user_id Status Code: {admin_ssoUsersGetCall4.status_code}")
            response = admin_ssoUsersGetCall4.text
            user_db_id = response[14:18]
        else:
            print(f"ERROR - GET /admin/users/user_id Status Code: {admin_ssoUsersGetCall4.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoUsersGetCall4.headers}\n')
            print(f'RESPONSE: {admin_ssoUsersGetCall4.text}\n')
        time.sleep(2)

        # PATCH /admin/users/{user_id}
        # user_id pulled from test setup sso users
        admin_ssoUsers_headers6 = {'Authorization': admin_access_token}
        admin_ssoUsers_payload6 = {'comment': 'api automated testing', "profileUpdate": {'email': test_user_emails[0],
                                'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                'phone': '555'+str(randint(2000000, 9999999)),
                                'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState, 'zip': var.CREDSapi.ssoZip}}
        admin_ssoUsersPatchCall2 = requests.patch(
            f'https://api-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}', headers=admin_ssoUsers_headers6, json=admin_ssoUsers_payload6)
        if admin_ssoUsersPatchCall2.status_code == 200:
            print(f"PATCH /admin/users/user_id Status Code: {admin_ssoUsersPatchCall2.status_code}")
        else:
            print(f"ERROR - PATCH /admin/users/user_id Status Code: {admin_ssoUsersPatchCall2.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoUsersPatchCall2.headers}\n')
            print(f'RESPONSE: {admin_ssoUsersPatchCall2.text}\n')
        time.sleep(2)

        # POST /admin/users/{user_id}/reset-password
        # user_id pulled from test setup sso users
        admin_resetPsw_headers = {'Authorization': admin_access_token}
        admin_resetPsw_payload = {'comment': 'automated testing'}
        admin_resetPswPostCall = requests.post(f'https://api-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}/reset-password', headers=admin_resetPsw_headers, json=admin_resetPsw_payload)
        if admin_resetPswPostCall.status_code == 200:
            print(f"POST /admin/users/user_id/reset-password Status Code: {admin_resetPswPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/users/user_id/reset-password Status Code: {admin_resetPswPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_resetPswPostCall.headers}\n')
            print(f'RESPONSE: {admin_resetPswPostCall.text}\n')
        time.sleep(2)

        # GET /admin/user-audits/{user_db_id}
        admin_userAudits_headers = {'Authorization': admin_access_token}
        admin_userAuditsGetCall = requests.get(f'https://api-{self.env}.nylservices.net/admin/user-audits/{user_db_id}', headers=admin_userAudits_headers)
        if admin_userAuditsGetCall.status_code == 200:
            print(f"GET /admin/user-audits/user_db_id Status Code: {admin_userAuditsGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/user-audits/user_db_id Status Code: {admin_userAuditsGetCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_userAuditsGetCall.headers}\n')
            print(f'RESPONSE: {admin_userAuditsGetCall.text}\n')
        time.sleep(2)

        # POST /admin/user-audits/{user_db_id}
        admin_userAudits_headers2 = {'Authorization': admin_access_token}
        admin_userAudits_payload2 = {'activity': 'api automated testing note', 'comment': 'api automated testing'}
        admin_userAuditsPostCall = requests.post(f'https://api-{self.env}.nylservices.net/admin/user-audits/{user_db_id}', headers=admin_userAudits_headers2, json=admin_userAudits_payload2)
        if admin_userAuditsPostCall.status_code == 200:
            print(f"GET /admin/user-audits/user_db_id Status Code: {admin_userAuditsPostCall.status_code}")
        else:
            print(f"ERROR - GET /admin/user-audits/user_db_id Status Code: {admin_userAuditsPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_userAuditsPostCall.headers}\n')
            print(f'RESPONSE: {admin_userAuditsPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/verify
        # user_id pulled from test setup sso users
        admin_bulkVerify_headers = {'Authorization': admin_access_token}
        admin_bulkVerify_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkVerifyPostCall = requests.post(f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/verify', headers=admin_bulkVerify_headers, json=admin_bulkVerify_payload)
        if admin_bulkVerifyPostCall.status_code == 200:
            print(f"POST /admin/pools/user_pool_id/users/_bulk/verify Status Code: {admin_bulkVerifyPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/verify Status Code: {admin_bulkVerifyPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkVerifyPostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkVerifyPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/unverify
        admin_bulkUnverify_headers = {'Authorization': admin_access_token}
        admin_bulkUnverify_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkUnverifyPostCall = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/unverify',
            headers=admin_bulkUnverify_headers, json=admin_bulkUnverify_payload)
        if admin_bulkUnverifyPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/unverify Status Code: {admin_bulkUnverifyPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/unverify Status Code: {admin_bulkUnverifyPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkUnverifyPostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkUnverifyPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/lock
        admin_bulkLock_headers = {'Authorization': admin_access_token}
        admin_bulkLock_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkLockPostCall = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/lock',
            headers=admin_bulkLock_headers, json=admin_bulkLock_payload)
        if admin_bulkLockPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/lock Status Code: {admin_bulkLockPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/lock Status Code: {admin_bulkLockPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkLockPostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkLockPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/unlock
        admin_bulkUnlock_headers = {'Authorization': admin_access_token}
        admin_bulkUnlock_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkUnlockPostCall = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/unlock',
            headers=admin_bulkUnlock_headers, json=admin_bulkUnlock_payload)
        if admin_bulkUnlockPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/unlock Status Code: {admin_bulkUnlockPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/unlock Status Code: {admin_bulkUnlockPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkUnlockPostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkUnlockPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/mark-for-deletion
        admin_bulkMarkDeletion_headers1 = {'Authorization': admin_access_token}
        admin_bulkMarkDeletion_payload1 = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkMarkDeletionPostCall1 = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/mark-for-deletion',
            headers=admin_bulkMarkDeletion_headers1, json=admin_bulkMarkDeletion_payload1)
        if admin_bulkMarkDeletionPostCall1.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/mark-for-deletion Status Code: {admin_bulkMarkDeletionPostCall1.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/mark-for-deletion Status Code: {admin_bulkMarkDeletionPostCall1.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkMarkDeletionPostCall1.headers}\n')
            print(f'RESPONSE: {admin_bulkMarkDeletionPostCall1.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/cancel-deletion
        admin_bulkCancelDeletion_headers = {'Authorization': admin_access_token}
        admin_bulkCancelDeletion_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkCancelDeletionPostCall = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/cancel-deletion',
            headers=admin_bulkCancelDeletion_headers, json=admin_bulkCancelDeletion_payload)
        if admin_bulkCancelDeletionPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/cancel-deletion Status Code: {admin_bulkCancelDeletionPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/cancel-deletion Status Code: {admin_bulkCancelDeletionPostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkCancelDeletionPostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkCancelDeletionPostCall.text}\n')
        time.sleep(2)

        # POST /admin/pools/{user_pool_id}/users/_bulk/purge
        #########
        # Test setup - marking users for deletion
        admin_bulkMarkDeletion_headers2 = {'Authorization': admin_access_token}
        admin_bulkMarkDeletion_payload2 = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkMarkDeletionPostCall2 = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/mark-for-deletion',
            headers=admin_bulkMarkDeletion_headers2, json=admin_bulkMarkDeletion_payload2)
        if admin_bulkMarkDeletionPostCall2.status_code == 200:
            pass
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/mark-for-deletion Status Code: {admin_bulkMarkDeletionPostCall2.status_code}")
            print("purge test setup cannot be completed because failed to mark test users for deletion")
            print(admin_bulkMarkDeletionPostCall2.text)
        time.sleep(2)
        #########
        admin_bulkPurge_headers = {'Authorization': admin_access_token}
        admin_bulkPurge_payload = {"comment": "automated testing", "users": [{"userId": test_user_subs[0]},{"userId": test_user_subs[1]},{"userId": test_user_subs[2]},{"userId": test_user_subs[3]},{"userId": test_user_subs[4]},{"userId": test_user_subs[5]},{"userId": test_user_subs[6]},{"userId": test_user_subs[7]},{"userId": test_user_subs[8]},{"userId": test_user_subs[9]}]}
        admin_bulkPurgePostCall = requests.post(
            f'https://api-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/purge',
            headers=admin_bulkPurge_headers, json=admin_bulkPurge_payload)
        if admin_bulkPurgePostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/purge Status Code: {admin_bulkPurgePostCall.status_code}")
            print(admin_bulkPurgePostCall.text)
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/purge Status Code: {admin_bulkPurgePostCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_bulkPurgePostCall.headers}\n')
            print(f'RESPONSE: {admin_bulkPurgePostCall.text}\n')
        time.sleep(2)

        # GET /admin/purged-users
        admin_ssoPurgedUsers_headers1 = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall1 = requests.get('https://api-' + self.env + '.nylservices.net/admin/purged-users', headers=admin_ssoPurgedUsers_headers1)
        if admin_ssoPurgedUsersGetCall1.status_code == 200:
            print(f"GET /admin/purged-users Status Code: {admin_ssoPurgedUsersGetCall1.status_code}")
            purged_user_db_id = admin_ssoPurgedUsersGetCall1.text[53:56]
            print(purged_user_db_id)
            print(admin_ssoPurgedUsersGetCall1.text)
        else:
            print(f"ERROR - GET /admin/purged-users Status Code: {admin_ssoPurgedUsersGetCall1.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoPurgedUsersGetCall1.headers}\n')
            print(f'RESPONSE: {admin_ssoPurgedUsersGetCall1.text}\n')
        time.sleep(2)

        # GET /admin/purged-users with params
        admin_ssoPurgedUsers_params2 = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoPurgedUsers_headers2 = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall2 = requests.get('https://api-' + self.env + '.nylservices.net/admin/purged-users', params=admin_ssoPurgedUsers_params2, headers=admin_ssoPurgedUsers_headers2)
        if admin_ssoPurgedUsersGetCall2.status_code == 200:
            print(f"GET /admin/purged-users with params Status Code: {admin_ssoPurgedUsersGetCall2.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users with params Status Code: {admin_ssoPurgedUsersGetCall2.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoPurgedUsersGetCall2.headers}\n')
            print(f'RESPONSE: {admin_ssoPurgedUsersGetCall2.text}\n')
        time.sleep(2)

        # GET /admin/purged-users with search terms
        # search_term (if searching)column, order (if sorting)
        admin_ssoPurgedUsers_params3 = {"search_term": test_user_emails[0], "limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoPurgedUsers_headers3 = {'Authorization': admin_access_token, "Accept": "application/json", "Content-Type": "application/json", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoPurgedUsersGetCall3 = requests.get('https://api-' + self.env + '.nylservices.net/admin/purged-users', params=admin_ssoPurgedUsers_params3, headers=admin_ssoPurgedUsers_headers3)
        if admin_ssoPurgedUsersGetCall3.status_code == 200:
            print(f"GET /admin/purged-users with search terms Status Code: {admin_ssoPurgedUsersGetCall3.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users with search terms Status Code: {admin_ssoPurgedUsersGetCall3.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoPurgedUsersGetCall3.headers}\n')
            print(f'RESPONSE: {admin_ssoPurgedUsersGetCall3.text}\n')
        time.sleep(2)

        # # GET /admin/purged-users/{user_db_id}
        # purged_user_db_id pulled from previous get purged user calll
        admin_ssoPurgedUsers_headers4 = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall4 = requests.get(f'https://api-{self.env}.nylservices.net/admin/purged-users/{purged_user_db_id}', headers=admin_ssoPurgedUsers_headers4)
        if admin_ssoPurgedUsersGetCall4.status_code == 200:
            print(f"GET /admin/purged-users/user_db_id Status Code: {admin_ssoPurgedUsersGetCall4.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users/user_db_id Status Code: {admin_ssoPurgedUsersGetCall4.status_code}")
            print(f'RESPONSE HEADERS: {admin_ssoPurgedUsersGetCall4.headers}\n')
            print(f'RESPONSE: {admin_ssoPurgedUsersGetCall4.text}\n')
        time.sleep(2)

        # POST /admin/logout
        admin_logout_headers = {'Authorization': admin_access_token}
        admin_logout_payload = {'accessToken': admin_access_token}
        admin_logoutCall = requests.post('https://api-' + self.env + '.nylservices.net/admin/logout', headers=admin_logout_headers, json=admin_logout_payload)
        if admin_logoutCall.status_code == 200:
            print(f"POST /admin/logout Status Code: {admin_logoutCall.status_code}")
        else:
            print(f"ERROR - POST /admin/logout Status Code: {admin_logoutCall.status_code}")
            print(f'RESPONSE HEADERS: {admin_logoutCall.headers}\n')
            print(f'RESPONSE: {admin_logoutCall.text}\n')

        # Clean up - clear test user from userpool
        print('\n\nAdmin API test complete\n\nTest clean up commencing')
        for email in test_user_emails:
            try:
                funct.purgeSSOemail(self, email)
            except:
                print('no test user ' + testemailSSO + ' found \n')


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    unittest.main(warnings='ignore')
    # if confTest.NYlottoBASE.report == "terminal":
    #     unittest.main(warnings='ignore')
    # elif confTest.NYlottoBASE.report == "html":
    #     unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))