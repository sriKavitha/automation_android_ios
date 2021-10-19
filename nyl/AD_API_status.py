from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
import requests, json           # Requests provides ability to hit API Json provides ability to encode & decode Json files
# import HtmlTestRunner

import var, funct, confTest     # Custom class for NYL

class NYLadmin(confTest.NYLadminBASE):

    def test_apiStatusCode(self):
        # [Documentation - Summary] Checks that response status code 200 is returned
        # for Admin Dash API endpoints

        testenv = self.env
        print("TESTING " + testenv + " ENVIRONMENT")

        if self.env == 'dev':
            client_id = '7o78gaj00d672ernobk1pll51p'
        elif self.env == 'qa':
            client_id = ''
        elif self.env == 'stage':
            client_id = ''

        if self.env == 'dev':
            user_pool_id = 'us-east-1_GFTjSQrHQ'
        elif self.env == 'qa':
            client_id = 'us-east-1_QZZDGaPyw'
        elif self.env == 'stage':
            client_id = 'us-east-1_v3S7DZTfs'
        ts = funct.timeStamp()
        # email for admin invite
        testemailAdmin = 'qa+admin@rosedigital.co'

        # time.sleep() added between calls so tests do not hit AWS Batch API limits

        driver = self.driver
        # url is pulled from confTest
        driver.get(self.admin_url)

        # Instructions for webdriver to read and input user data via the info on the .txt doc.
        # Credentials are localized to one instance via the var file
        funct.waitAndSend(driver, var.adminLoginVar.email, var.CREDSadmin.superadmin_username)
        funct.waitAndSend(driver, var.adminLoginVar.password, var.CREDSadmin.superadmin_psw)
        funct.waitAndClick(driver, var.adminLoginVar.signin_button)
        cookie_IdToken = driver.get_cookie('NYL_ADMIN_IDENTITY_TOKEN')  # grabs dictionary of the cookie with name = 'NYL_ADMIN_IDENTITY_TOKEN'
        cookie_AccessToken = driver.get_cookie('NYL_ADMIN_ACCESS_TOKEN')
        cookie_gcl_au = driver.get_cookie('_gcl_au')
        admin_id_token = (cookie_IdToken['value'])
        admin_access_token = (cookie_AccessToken['value'])
        admin_gcl_cookie = (cookie_gcl_au['value'])
        time.sleep(1)

        # List of Admin endpoints
        # TODO POST /admin/login
        # admin_login_params = {'client_id': client_id, 'response_type': 'token', 'scope': 'email openid phone aws.cognito.signin.user.admin', 'redirect_uri': 'https://admin-dev.nylservices.net/login-response'}
        # admin_login_formdata= {"username": var.adminLoginVar.email, "password": var.adminLoginVar.password}
        # # 'https://admin-dev.nylservices.net/'
        # # admin_loginCall = requests.post('https://admin-' + self.env + '.nylservices.net/admin/login', data=admin_login_formdata, params=admin_login_params)
        # if admin_loginCall.status_code == 302:
        #     print('PASS: Expected redirect')
        #     print(f"POST /admin/login (SSO User) Status Code: {admin_loginCall.status_code}")
        # else:
        #     print(f"ERROR - POST /admin/login Status Code: {admin_loginCall.status_code}")
        #     print(admin_loginCall.text)

        # TODO GET /admin/login-response
        admin_login_response_headers = {"cookie": "_gcl_au="+admin_gcl_cookie}
        admin_loginResponseCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/login-response', headers=admin_login_response_headers)
        if admin_loginResponseCall.status_code == 200:
            print(f"GET /admin/login-response Status Code: {admin_loginResponseCall.status_code}")
        else:
            print(f"ERROR - GET /admin/login-response Status Code: {admin_loginResponseCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/admin_users
        admin_adminUsers_headers = {'Authorization': admin_access_token}
        admin_adminUsersCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/admin_users', headers=admin_adminUsers_headers)
        if admin_adminUsersCall.status_code == 200:
            print(f"GET /admin/admin_users Status Code: {admin_adminUsersCall.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users Status Code: {admin_adminUsersCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/admin_users with params
        admin_adminUsers_params = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_adminUsers_headers = {'Authorization': admin_access_token}
        admin_adminUsersCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/admin_users', params=admin_adminUsers_params, headers=admin_adminUsers_headers)
        if admin_adminUsersCall.status_code == 200:
            print(f"GET /admin/admin_users with Params Status Code: {admin_adminUsersCall.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users with Params Status Code: {admin_adminUsersCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/admin_users with search terms
        admin_adminUsers_params = {"search_term": "e", "limit": 10, "offset": 0, "column": "", "order": ""}
        admin_adminUsers_headers = {'Authorization': admin_access_token}
        admin_adminUsersCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/admin_users', params=admin_adminUsers_params, headers=admin_adminUsers_headers)
        if admin_adminUsersCall.status_code == 200:
            print(f"GET /admin/admin_users with Search Term Status Code: {admin_adminUsersCall.status_code}")
        else:
            print(f"ERROR - GET /admin/admin_users with Search Term Status Code: {admin_adminUsersCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/invite
        admin_invite_headers = {'Authorization': admin_access_token}
        admin_invite_payload = {"firstName": "QA", "lastName": "Tester", "phone": "3472929732", "email": testemailAdmin, "isSuperadmin": "false"}
        admin_inviteCall = requests.post('https://admin-' + self.env + '.nylservices.net/admin/invite',
                                            headers=admin_invite_headers, json=admin_invite_payload)
        if admin_inviteCall.status_code == 200:
            print(f"POST /admin/invite Status Code: {admin_inviteCall.status_code}")
        else:
            print(f"ERROR - POST /admin/invite Status Code: {admin_inviteCall.status_code}")
        time.sleep(1)

        # TODO PATCH /admin/admin_users/{user_id}
        if self.env == 'dev':
            admin_user_id = '531899f9-9b54-4e6e-a0fc-1b6ec139bd7e'
        # elif self.env == 'qa':
        #     admin_user_id =
        # elif self.env == 'stage':
        #     admin_user_id =
        # Header:
        # Payload:
        admin_adminPatch_headers = {'Authorization': admin_access_token}
        admin_adminPatch_payload = {"roleUpdate": {"role": "csr"}, "profileUpdate": {"firstName": "QA", "lastName": "Tester", "phone": "3472929732"}}
        admin_adminPatchCall = requests.patch(f'https://admin-{self.env}.nylservices.net/admin/admin_users/{admin_user_id}',
                                            headers=admin_adminPatch_headers, json=admin_adminPatch_payload)
        if admin_adminPatchCall.status_code == 200:
            print(f"PATCH /admin/admin_users/user_id Status Code: {admin_adminPatchCall.status_code}")
        else:
            print(f"ERROR - PATCH /admin/admin_users/user_id Status Code: {admin_adminPatchCall.status_code}")
        time.sleep(1)

        # TODO PUT /admin/admin_users/{user_id}/status
        admin_adminStatus_headers = {'Authorization': admin_access_token}
        admin_adminStatus_payload = {"enabled": "false"}
        admin_adminStatusCall = requests.put(
            f'https://admin-{self.env}.nylservices.net/admin/admin_users/{admin_user_id}/status',
            headers=admin_adminStatus_headers, json=admin_adminStatus_payload)
        if admin_adminStatusCall.status_code == 200:
            print(f"PUT /admin/admin_users/user_id/status Status Code: {admin_adminStatusCall.status_code}")
        else:
            print(f"ERROR - PUT /admin/admin_users/user_id/status Status Code: {admin_adminStatusCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/features
        admin_features_headers = {'Authorization': admin_access_token}
        admin_featuresGetCall = requests.get(
            f'https://admin-{self.env}.nylservices.net/admin/features',
            headers=admin_features_headers)
        if admin_featuresGetCall.status_code == 200:
            print(f"GET /admin/features Status Code: {admin_featuresGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/features Status Code: {admin_featuresGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/features/ticket-scan
        admin_ticketscan_headers = {'Authorization': admin_access_token}
        admin_ticketscanGetCall = requests.get(
            f'https://admin-{self.env}.nylservices.net/admin/features/ticket-scan',
            headers=admin_ticketscan_headers)
        if admin_ticketscanGetCall.status_code == 200:
            print(f"GET /admin/features/ticket-scan Status Code: {admin_ticketscanGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/features/ticket-scan Status Code: {admin_ticketscanGetCall.status_code}")
        time.sleep(1)

        # TODO PUT /admin/features/ticket-scan
        admin_ticketscan_headers = {'Authorization': admin_access_token}
        admin_ticketscan_payload = {'scanCountLimit': 2000, 'isEnabled': 'true', 'comment': 'api testing', 'isUnlimited': 'false'}
        admin_ticketscanPutCall = requests.put(
            f'https://admin-{self.env}.nylservices.net/admin/features/ticket-scan',
            headers=admin_ticketscan_headers, json=admin_ticketscan_payload)
        if admin_ticketscanPutCall.status_code == 200:
            print(f"PUT /admin/features/ticket-scan Status Code: {admin_ticketscanPutCall.status_code}")
        else:
            print(f"ERROR - PUT /admin/features/ticket-scan Status Code: {admin_ticketscanPutCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/features-audit-log
        admin_featuresAudit_headers = {'Authorization': admin_access_token}
        admin_featuresAuditGetCall = requests.get(f'https://admin-{self.env}.nylservices.net/admin/features-audit-log', headers=admin_featuresAudit_headers)
        if admin_featuresAuditGetCall.status_code == 200:
            print(f"GET /admin/features-audit-log Status Code: {admin_featuresAuditGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/features-audit-log Status Code: {admin_featuresAuditGetCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/features-audit-log
        admin_featuresAudit_headers = {'Authorization': admin_access_token}
        admin_featuresAudit_payload = {'comment': 'automated testing'}
        admin_featuresAuditPostCall = requests.post(f'https://admin-{self.env}.nylservices.net/admin/features-audit-log', headers=admin_featuresAudit_headers, json=admin_featuresAudit_payload)
        if admin_featuresAuditPostCall.status_code == 200:
            print(f"POST /admin/features-audit-log Status Code: {admin_featuresAuditPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/features-audit-log Status Code: {admin_featuresAuditPostCall.status_code}")
        time.sleep(1)


        # TODO create users to manipulate in the admin dash
        # grabbing entry info through localized var/ funct files
        if testenv == 'dev':
            client_id = var.CREDSapi.devSSOcid
        elif testenv == 'qa':
            client_id = var.CREDSapi.qaSSOcid
        elif testenv == 'stage':
            client_id = var.CREDSapi.stageSSOcid

        # Create SSO user via register-verify api call,
        # grab and decrypt cognito sub from JSON response
        # for admin user id api calls further down
        # create users list pairs with email address and cognito sub
        # for api calls further down
        test_user_emails = []
        test_user_subs = []
        i = 1
        num_test_users = 11
        while i < num_test_users:
            ts = funct.timeStamp()
            testemailSSO = 'qa+sso' + ts + '@rosedigital.co'
            sso_register_payload = {'clientId': client_id, 'email': testemailSSO, 'password': var.CREDSapi.ssoPW,
                                    'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                    'phone': var.CREDSapi.ssoPhone,
                                    'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                    'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                    'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState,
                                    'zip': var.CREDSapi.ssoZip, 'ssn4': var.CREDSapi.ssoSSN, 'noSsn4': 'false'}
            sso_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                             json=sso_register_payload)
            # [Documentation - detail] grabbing the idToken from the registration response body
            print(sso_registerCall.text)
            registerResponse = []
            quoted = re.compile('"(.*?)"')
            for value in quoted.findall(sso_registerCall.text):
                # print(value)
                registerResponse.append(value)
            sso_register_id_token = registerResponse[9]
            # print(sso_registerCall.text)
            # print(sso_register_id_token)
            import jwt
            encoded = sso_register_id_token
            decoded = jwt.decode(encoded, options={"verify_signature": False})  # decoding the idToken
            test_user_emails.append(decoded['email'])
            test_user_subs.append(decoded['sub'])
            i += 1
        print(test_user_emails)
        print(test_user_subs)

        # TODO GET /admin/users
        admin_ssoUsers_headers = {'Authorization': admin_access_token}
        admin_ssoUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/users', headers=admin_ssoUsers_headers)
        if admin_ssoUsersGetCall.status_code == 200:
            print(f"GET /admin/users Status Code: {admin_ssoUsersGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/users Status Code: {admin_ssoUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/users with params
        # https://api-dev.nylservices.net/admin/users?limit=10&offset=0&column=&order=
        admin_ssoUsers_params = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoUsers_headers = {'Authorization': admin_access_token}
        admin_ssoUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/users', params=admin_ssoUsers_params , headers=admin_ssoUsers_headers)
        if admin_ssoUsersGetCall.status_code == 200:
            print(f"GET /admin/users with params Status Code: {admin_ssoUsersGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/users with params Status Code: {admin_ssoUsersGetCall.status_code}")
        time.sleep(1)


        # TODO GET /admin/users with search terms
        # search_term (if searching)column, order (if sorting)
        admin_ssoUsers_params = {"search_term": testemailSSO, "limit": 10, "offset": 0, "column": "", "order": ""}
        # admin_ssoUsers_headers = {'Authorization': admin_access_token, "scheme": "https", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "origin": "https://admin-dev.nylservices.net", "referer": "https://admin-dev.nylservices.net/", "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', "sec-ch-ua-platform": "macOS", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoUsers_headers = {'Authorization': admin_access_token, "Accept": "application/json", "Content-Type": "application/json", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/users', params=admin_ssoUsers_params, headers=admin_ssoUsers_headers)
        if admin_ssoUsersGetCall.status_code == 200:
            print(f"GET /admin/users with search terms Status Code: {admin_ssoUsersGetCall.status_code}")
            # print(admin_ssoUsersGetCall.text)
            # print(admin_ssoUsersGetCall)
            # print(repr(admin_ssoUsersGetCall))
            # print(admin_ssoUsersGetCall.json())
        else:
            print(f"ERROR - GET /admin/users with search terms Status Code: {admin_ssoUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/users/{user_id}
        # user_id pulled from previous sso register-verify api call
        # admin_ssoUsers_headers = {'Authorization': admin_access_token}
        admin_ssoUsers_headers = {'Authorization': admin_access_token, "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br",
                                  "Connection": "keep-alive",
                                  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoUsersGetCall = requests.get(f'https://admin-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}', headers=admin_ssoUsers_headers)
        if admin_ssoUsersGetCall.status_code == 200:
            print(f"GET /admin/users/user_id Status Code: {admin_ssoUsersGetCall.status_code}")
            print(admin_ssoUsersGetCall.text)
            print(admin_ssoUsersGetCall)
            print(repr(admin_ssoUsersGetCall))
            print(admin_ssoUsersGetCall.json())
        else:
            print(f"ERROR - GET /admin/users/user_id Status Code: {admin_ssoUsersGetCall.status_code}")
        time.sleep(1)

        # TODO PATCH /admin/users/{user_id}
        admin_ssoUsers_headers = {'Authorization': admin_access_token}
        admin_ssoUsers_payload = {'comment': 'api automated testing', "profileUpdate": {'email': test_user_emails[0],
                                'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                'phone': var.CREDSapi.ssoPhone,
                                'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState, 'zip': var.CREDSapi.ssoZip}}
        admin_ssoUsersPatchCall = requests.patch(
            f'https://admin-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}', headers=admin_ssoUsers_headers, json=admin_ssoUsers_payload)
        if admin_ssoUsersPatchCall.status_code == 200:
            print(f"PATCH /admin/users/user_id Status Code: {admin_ssoUsersPatchCall.status_code}")
        else:
            print(f"ERROR - PATCH /admin/users/user_id Status Code: {admin_ssoUsersPatchCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/users/{user_id}/reset-password
        # user_id pulled from previous sso register-verify api call
        admin_resetPsw_headers = {'Authorization': admin_access_token}
        admin_resetPsw_payload = {'comment': 'automated testing'}
        admin_resetPswPostCall = requests.post(f'https://admin-{self.env}.nylservices.net/admin/users/{test_user_subs[0]}/reset-password', headers=admin_resetPsw_headers, json=admin_resetPsw_payload)
        if admin_resetPswPostCall.status_code == 200:
            print(f"POST /admin/users/user_id/reset-password Status Code: {admin_resetPswPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/users/user_id/reset-password Status Code: {admin_resetPswPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/verify
        admin_bulkVerify_headers = {'Authorization': admin_access_token}
        admin_bulkVerify_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                               "userId": test_user_subs[1],
                                                                               "userId": test_user_subs[2],
                                                                               "userId": test_user_subs[3],
                                                                               "userId": test_user_subs[4],
                                                                               "userId": test_user_subs[5],
                                                                               "userId": test_user_subs[6],
                                                                               "userId": test_user_subs[7],
                                                                               "userId": test_user_subs[8],
                                                                               "userId": test_user_subs[9],
                                                                               }]}
        admin_bulkVerifyPostCall = requests.post(f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/verify', headers=admin_bulkVerify_headers, json=admin_bulkVerify_payload)
        if admin_bulkVerifyPostCall.status_code == 200:
            print(f"POST /admin/pools/user_pool_id/users/_bulk/verify Status Code: {admin_bulkVerifyPostCall.status_code}")
        else:
            print(f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/verify Status Code: {admin_bulkVerifyPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/unverify
        admin_bulkUnverify_headers = {'Authorization': admin_access_token}
        admin_bulkUnverify_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                               "userId": test_user_subs[1],
                                                                               "userId": test_user_subs[2],
                                                                               "userId": test_user_subs[3],
                                                                               "userId": test_user_subs[4],
                                                                               "userId": test_user_subs[5],
                                                                               "userId": test_user_subs[6],
                                                                               "userId": test_user_subs[7],
                                                                               "userId": test_user_subs[8],
                                                                               "userId": test_user_subs[9],
                                                                               }]}
        admin_bulkUnverifyPostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/unverify',
            headers=admin_bulkUnverify_headers, json=admin_bulkUnverify_payload)
        if admin_bulkUnverifyPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/unverify Status Code: {admin_bulkUnverifyPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/unverify Status Code: {admin_bulkUnverifyPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/lock
        admin_bulkLock_headers = {'Authorization': admin_access_token}
        admin_bulkLock_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                               "userId": test_user_subs[1],
                                                                               "userId": test_user_subs[2],
                                                                               "userId": test_user_subs[3],
                                                                               "userId": test_user_subs[4],
                                                                               "userId": test_user_subs[5],
                                                                               "userId": test_user_subs[6],
                                                                               "userId": test_user_subs[7],
                                                                               "userId": test_user_subs[8],
                                                                               "userId": test_user_subs[9],
                                                                               }]}
        admin_bulkLockPostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/lock',
            headers=admin_bulkLock_headers, json=admin_bulkLock_payload)
        if admin_bulkLockPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/lock Status Code: {admin_bulkLockPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/lock Status Code: {admin_bulkLockPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/unlock
        admin_bulkUnlock_headers = {'Authorization': admin_access_token}
        admin_bulkUnlock_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                               "userId": test_user_subs[1],
                                                                               "userId": test_user_subs[2],
                                                                               "userId": test_user_subs[3],
                                                                               "userId": test_user_subs[4],
                                                                               "userId": test_user_subs[5],
                                                                               "userId": test_user_subs[6],
                                                                               "userId": test_user_subs[7],
                                                                               "userId": test_user_subs[8],
                                                                               "userId": test_user_subs[9],
                                                                               }]}
        admin_bulkUnlockPostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/unlock',
            headers=admin_bulkUnlock_headers, json=admin_bulkUnlock_payload)
        if admin_bulkUnlockPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/unlock Status Code: {admin_bulkUnlockPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/unlock Status Code: {admin_bulkUnlockPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/mark-for-deletion
        admin_bulkMarkDeletion_headers = {'Authorization': admin_access_token}
        admin_bulkMarkDeletion_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                               "userId": test_user_subs[1],
                                                                               "userId": test_user_subs[2],
                                                                               "userId": test_user_subs[3],
                                                                               "userId": test_user_subs[4],
                                                                               "userId": test_user_subs[5],
                                                                               "userId": test_user_subs[6],
                                                                               "userId": test_user_subs[7],
                                                                               "userId": test_user_subs[8],
                                                                               "userId": test_user_subs[9],
                                                                               }]}
        admin_bulkMarkDeletionPostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/mark-for-deletion',
            headers=admin_bulkMarkDeletion_headers, json=admin_bulkMarkDeletion_payload)
        if admin_bulkMarkDeletionPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/mark-for-deletion Status Code: {admin_bulkMarkDeletionPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/mark-for-deletion Status Code: {admin_bulkMarkDeletionPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/cancel-deletion
        admin_bulkCancelDeletion_headers = {'Authorization': admin_access_token}
        admin_bulkCancelDeletion_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                                     "userId": test_user_subs[1],
                                                                                     "userId": test_user_subs[2],
                                                                                     "userId": test_user_subs[3],
                                                                                     "userId": test_user_subs[4],
                                                                                     "userId": test_user_subs[5],
                                                                                     "userId": test_user_subs[6],
                                                                                     "userId": test_user_subs[7],
                                                                                     "userId": test_user_subs[8],
                                                                                     "userId": test_user_subs[9],
                                                                                     }]}
        admin_bulkCancelDeletionPostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/cancel-deletion',
            headers=admin_bulkCancelDeletion_headers, json=admin_bulkCancelDeletion_payload)
        if admin_bulkCancelDeletionPostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/cancel-deletion Status Code: {admin_bulkCancelDeletionPostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/cancel-deletion Status Code: {admin_bulkCancelDeletionPostCall.status_code}")
        time.sleep(1)

        # TODO POST /admin/pools/{user_pool_id}/users/_bulk/purge
        admin_bulkPurge_headers = {'Authorization': admin_access_token}
        admin_bulkPurge_payload = {'comment': 'automated testing', "users": [{"userId": test_user_subs[0],
                                                                                     "userId": test_user_subs[1],
                                                                                     "userId": test_user_subs[2],
                                                                                     "userId": test_user_subs[3],
                                                                                     "userId": test_user_subs[4],
                                                                                     "userId": test_user_subs[5],
                                                                                     "userId": test_user_subs[6],
                                                                                     "userId": test_user_subs[7],
                                                                                     "userId": test_user_subs[8],
                                                                                     "userId": test_user_subs[9],
                                                                                     }]}
        admin_bulkPurgePostCall = requests.post(
            f'https://admin-{self.env}.nylservices.net/admin/pools/{user_pool_id}/users/_bulk/purge',
            headers=admin_bulkPurge_headers, json=admin_bulkPurge_payload)
        if admin_bulkPurgePostCall.status_code == 200:
            print(
                f"POST /admin/pools/user_pool_id/users/_bulk/purge Status Code: {admin_bulkPurgePostCall.status_code}")
        else:
            print(
                f"ERROR - POST /admin/pools/user_pool_id/users/_bulk/purge Status Code: {admin_bulkPurgePostCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/purged-users
        admin_ssoPurgedUsers_headers = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/purged-users', headers=admin_ssoPurgedUsers_headers)
        if admin_ssoPurgedUsersGetCall.status_code == 200:
            print(f"GET /admin/purged-users Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/purged-users with params
        # https://api-dev.nylservices.net/admin/users?limit=10&offset=0&column=&order=
        admin_ssoPurgedUsers_params = {"limit": 10, "offset": 0, "column": "", "order": ""}
        admin_ssoPurgedUsers_headers = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/purged-users', params=admin_ssoPurgedUsers_params, headers=admin_ssoPurgedUsers_headers)
        if admin_ssoPurgedUsersGetCall.status_code == 200:
            print(f"GET /admin/purged-users with params Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users with params Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/purged-users with search terms
        # search_term (if searching)column, order (if sorting)
        admin_ssoPurgedUsers_params = {"search_term": testemailSSO, "limit": 10, "offset": 0, "column": "", "order": ""}
        # admin_ssoPurgedUsers_headers = {'Authorization': admin_access_token, "scheme": "https", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip, deflate, br", "origin": "https://admin-dev.nylservices.net", "referer": "https://admin-dev.nylservices.net/", "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', "sec-ch-ua-platform": "macOS", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoPurgedUsers_headers = {'Authorization': admin_access_token, "Accept": "application/json", "Content-Type": "application/json", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"}
        admin_ssoPurgedUsersGetCall = requests.get('https://admin-' + self.env + '.nylservices.net/admin/purged-users', params=admin_ssoPurgedUsers_params, headers=admin_ssoPurgedUsers_headers)
        if admin_ssoPurgedUsersGetCall.status_code == 200:
            print(f"GET /admin/purged-users with search terms Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
            print(admin_ssoPurgedUsersGetCall.text)
            # print(admin_ssoPurgedUsersGetCall.json())
        else:
            print(f"ERROR - GET /admin/purged-users with search terms Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/purged-users/{user_db_id}
        # user_id pulled from previous sso register-verify api call
        admin_ssoPurgedUsers_headers = {'Authorization': admin_access_token}
        admin_ssoPurgedUsersGetCall = requests.get(f'https://admin-{self.env}.nylservices.net/admin/purged-users/{test_user_subs[0]}', headers=admin_ssoPurgedUsers_headers)
        if admin_ssoPurgedUsersGetCall.status_code == 200:
            print(f"GET /admin/purged-users/user_id Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        else:
            print(f"ERROR - GET /admin/purged-users/user_id Status Code: {admin_ssoPurgedUsersGetCall.status_code}")
        time.sleep(1)

        # TODO GET /admin/user-audits/{user_db_id}
        # Header:{
        # "Authorization": "access_token"
        # }
        # admin_useraudits_headers = {'Authorization': admin_access_token}
        # admin_userAuditsGetCall = requests.get(f'https://admin-{self.env}.nylservices.net/admin/user-audits/{test_user_subs[0]}', headers=admin_useraudits_headers)
        # if admin_userAuditsGetCall.status_code == 200:
        #     print(f"/admin/user-audits/user_db_id Status Code: {admin_userAuditsGetCall.status_code}")
        # else:
        #     print(f"ERROR - /admin/user-audits/user_db_id Status Code: {admin_userAuditsGetCall.status_code}")
        # time.sleep(1)

        # TODO POST /admin/user-audits/{user_db_id}
        # Header:{
        # "Authorization": "access_token"
        # }
        # Payload: {
        #     activity,
        #     comment
        # }
        # admin_useraudits_headers = {'Authorization': admin_access_token}
        # admin_useraudits_payload = {'activity': 'api automated testing note', 'comment': 'api automated testing'}
        # admin_userAuditsPostCall = requests.post(f'https://admin-{self.env}.nylservices.net/admin/user-audits/{test_user_subs[0]}', headers=admin_useraudits_headers, json=admin_useraudits_payload)
        # if admin_userAuditsPostCall.status_code == 200:
        #     print(f"/admin/user-audits/user_db_id Status Code: {admin_userAuditsPostCall.status_code}")
        # else:
        #     print(f"ERROR - /admin/user-audits/user_db_id Status Code: {admin_userAuditsPostCall.status_code}")
        # time.sleep(1)

        # TODO POST /admin/logout
        admin_logout_headers = {'Authorization': admin_access_token}
        admin_logout_payload = {'accessToken': admin_access_token}
        admin_logoutCall = requests.post('https://admin-' + self.env + '.nylservices.net/admin/logout', headers=admin_logout_headers, json=admin_logout_payload)
        if admin_logoutCall.status_code == 200:
            print(f"POST /admin/logout Status Code: {admin_logoutCall.status_code}")
        else:
            print(f"ERROR - POST /admin/logout Status Code: {admin_logoutCall.status_code}")

        print('\n\nAdmin Dash API test complete\n\n')


# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    unittest.main(warnings='ignore')
    # if confTest.NYlottoBASE.report == "terminal":
    #     unittest.main(warnings='ignore')
    # elif confTest.NYlottoBASE.report == "html":
    #     unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))