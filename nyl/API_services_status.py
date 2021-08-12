from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
import requests, json           # Requests provides ability to hit API Json provides ability to encode & decode Json files
import HTMLTestRunner

import var, funct, confTest     # Custom class for NYL

class NYLServices(confTest.NYLservicesBASE):

    def test_apiStatusCode(self):
        # [Documentation - Summary] Checks that response status code 200 is returned
        # for Nylservices APIs with proper payloads in requests
        # For use with Creds file version: api01122021.txt

        # time.sleep() added between calls so tests do not hit AWS Batch API limits

        testenv = self.env

        ts = funct.timeStamp()
        # email for ssn registration
        testemailSSO = 'qa+sso' + ts + '@rosedigital.co'
        # email for mobile app registration
        testemailMOB = 'qa+mobile' + ts + '@rosedigital.co'

        # Check for existing test SSO user and wipe it from userpool prior to register api call
        try:
            nylAdminDash.funct.purgeSSO(self, testemailSSO)
            print('test user ' + testemailSSO + ' purged \n')
        except:
            print('no test user ' + testemailSSO + ' found \n')
        # Check for existing test Mobile user and wipe it from userpool prior to register api call
        try:
            funct.purgeMobile(self, testemailMOB)
            print('test user ' + testemailMOB + ' purged \n')
        except:
            print('no test user ' + testemailMOB + ' found \n')

        print('Current environment = ' + testenv)

        # grabbing entry info through localized var/ funct files
        if testenv == 'dev':
            client_id = var.CREDSapi.devSSOcid
            x_api_key = var.CREDSapi.devSSOxkey
            handle_govid_code = var.CREDSapi.devSSOhgcode
            m_client_id = var.CREDSapi.devMOBILEcid
            m_x_api_key = var.CREDSapi.devMOBILExkey
            m_fcm_token = var.CREDSapi.devFCMtoken
        elif testenv == 'qa':
            client_id = var.CREDSapi.qaSSOcid
            x_api_key = var.CREDSapi.qaSSOxkey
            handle_govid_code = var.CREDSapi.qaSSOhgcode
            m_client_id = var.CREDSapi.qaMOBILEcid
            m_x_api_key = var.CREDSapi.qaMOBILExkey
            m_fcm_token = var.CREDSapi.qaFCMtoken
        elif testenv == 'stage':
            client_id = var.CREDSapi.stageSSOcid
            x_api_key = var.CREDSapi.stageSSOxkey
            m_client_id = var.CREDSapi.stageMOBILEcid
            m_x_api_key = var.CREDSapi.stageMOBILExkey
            m_fcm_token = var.CREDSapi.stageFCMtoken

        # [Documentation - detail] setting up an api call using the requests method
        # [Documentation - detail] setting headers to let api know that we have proper permissions to run api call
        # [Documentation - detail] setting payload in json body in the api call

        # POST /sso/register-verify (SSO User)
        sso_register_payload = {'clientId': client_id, 'email': testemailSSO, 'password': var.CREDSapi.ssoPW,
                                'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                'phone': var.CREDSapi.ssoPhone,
                                'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState,
                                'zip': var.CREDSapi.ssoZip, 'ssn4': var.CREDSapi.ssoSSN, 'noSsn4': 'false'}
        sso_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                         json=sso_register_payload)
        if sso_registerCall.status_code == 200:
            print('POST /sso/register-verify (SSN Registration) Status Code: ' + str(sso_registerCall.status_code))
        else:
            print("ERROR - POST /sso/register-verify (SSN Registration) Status Code: ")
            print(sso_registerCall.status_code)
            print(sso_registerCall.text)

        # [Documentation - detail] grabbing the accessToken and refreshToken from the registration response body for use in later api calls
        registerResponse = []
        quoted = re.compile('"(.*?)"')
        for value in quoted.findall(sso_registerCall.text):
            # print(value)
            registerResponse.append(value)
        sso_register_access_token = registerResponse[2]
        sso_register_refresh_token = registerResponse[7]
        # For debugging token issues
        # print(sso_registerCall.text)
        # print(sso_register_access_token)
        # print(sso_register_refresh_token)

        # [Documentation - detail] Conditional check due to IDDW verification dependency with user verification
        if '"hardFail":true' in str(sso_registerCall.text):
            print('ERROR - IDDW Verification failed for user and user not created.\nRegistration response = ')
            print(sso_registerCall.text)
            raise Exception('Failed user creation. Unable to proceed further. Change test user data in creds file.')

        # POST /sso/refresh-token
        time.sleep(1)
        refresh_token_headers = {"x-api-key": x_api_key}
        refresh_token_payload = {"clientId": client_id, "refreshToken": sso_register_refresh_token}
        refreshTokenCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/refresh-token', headers=refresh_token_headers,
                                        json=refresh_token_payload)
        if refreshTokenCall.status_code == 200:
            print("POST /sso/refresh-token Status Code: " + str(refreshTokenCall.status_code))
        else:
            print("ERROR - POST /sso/refresh-token Status Code: ")
            print(refreshTokenCall.status_code)
            print(refreshTokenCall.text)

        # PUT /sso/register-verify (SSN Confirmation)
        time.sleep(1)
        ssn_confirm_payload = {"ssnConfirmation": {"ssn": "1111"}}
        ssn_confirm_headers = {'Authorization': sso_register_access_token}
        ssnConfirmCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify', headers=ssn_confirm_headers,
                                 json=ssn_confirm_payload)
        if ssnConfirmCall.status_code == 200:
            print("PUT /sso/register-verify (SSN Confirmation) Status Code: " + str(ssnConfirmCall.status_code))
        else:
            print("ERROR - PUT /sso/register-verify (SSN Confirmation) Status Code: ")
            print(ssnConfirmCall.status_code)
            print(ssnConfirmCall.text)

        # POST /sso/phone-code-gen
        time.sleep(1)
        phone_gen_payload = {"type": "sms"}
        phone_gen_headers = {'Authorization': sso_register_access_token}
        phoneGenCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/phone-code-gen', headers=phone_gen_headers,
                                 json=phone_gen_payload)
        if phoneGenCall.status_code == 200:
            print("POST /sso/phone-code-gen Status Code: " + str(phoneGenCall.status_code))
        else:
            print("ERROR - POST /sso/phone-code-gen Status Code: ")
            print(phoneGenCall.status_code)
            print(phoneGenCall.text)

        # PUT /sso/register-verify (Phone Confirmation)
        time.sleep(1)
        phone_confirm_payload = {"phoneConfirmation": {"asi": "true", "pincode": "1111", "pinType": "sms"}}
        phone_confirm_headers = {'Authorization': sso_register_access_token}
        phoneConfirmCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify', headers=phone_confirm_headers,
                                 json=phone_confirm_payload)
        if phoneConfirmCall.status_code == 200:
            print("PUT /sso/register-verify (Phone Confirmation) Status Code: " + str(phoneConfirmCall.status_code))
        else:
            print("ERROR - PUT /sso/register-verify (Phone Confirmation) Status Code: ")
            print(phoneConfirmCall.status_code)
            print(phoneConfirmCall.text)

        # PUT /sso/register-verify (Profile Update)
        time.sleep(1)
        profile_update_headers = {'Authorization': sso_register_access_token}
        profile_update_payload = {'profileUpdate': {'verify': 'true', 'firstName': var.CREDSapi.ssoFName, 'lastName': var.CREDSapi.ssoLName,
                                'phone': var.CREDSapi.ssoPhone,
                                'birthdate': var.CREDSapi.ssoDOBmonth + '/' + var.CREDSapi.ssoDOBDate + '/' + var.CREDSapi.ssoDOBYear,
                                'streetNumber': var.CREDSapi.ssoHNum, 'street': var.CREDSapi.ssoStreet,
                                'city': var.CREDSapi.ssoCity, 'state': var.CREDSapi.ssoState,
                                'zip': var.CREDSapi.ssoZip}}
        sso_profileUpdateCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                              headers=profile_update_headers, json=profile_update_payload)
        if sso_profileUpdateCall.status_code == 200:
            print("PUT /sso/register-verify (Profile Update) Status Code: " + str(sso_profileUpdateCall.status_code))
        else:
            print("ERROR - POST /sso/register-verify (Profile Update) Status Code: ")
            print(sso_profileUpdateCall.status_code)
            print(sso_profileUpdateCall.text)

        # TODO this request needs to be refactored for STAGE as the handle_govid_code must be dynamically generated
        # PUT /sso/handle-govid-response
        time.sleep(1)
        if testenv == 'stage':
            pass
        elif testenv == 'dev' or 'qa':
            handle_govid_payload = {"code": handle_govid_code, "govIdType": "usdl-desktop"}
            handle_govid_headers = {'Authorization': sso_register_access_token}
            handleGovidCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/handle-govid-response', headers=handle_govid_headers,
                                     json=handle_govid_payload)
            if handleGovidCall.status_code == 200:
                print("PUT /sso/handle-govid-response Status Code: " + str(handleGovidCall.status_code))
            else:
                print("ERROR - PUT /sso/handle-govid-response Status Code: ")
                print(handleGovidCall.status_code)
                print(handleGovidCall.text)

        # GET /users
        time.sleep(1)
        users_headers = {'Authorization': sso_register_access_token}
        usersGetCall = requests.get('https://api-' + self.env + '.nylservices.net/users', headers=users_headers)
        if usersGetCall.status_code == 200:
            print("GET /users Status Code: " + str(usersGetCall.status_code))
        else:
            print("ERROR - GET /users Status Code: ")
            print(usersGetCall.status_code)
            print(usersGetCall.text)

        # POST /sso/login (SSO user)
        time.sleep(1)
        sso_login_payload = {"email": testemailSSO, "clientId": client_id, "password": var.CREDSapi.ssoPW}
        sso_loginCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/login', json=sso_login_payload)
        if sso_loginCall.status_code == 200:
            print("PUT /sso/login (SSO User) Status Code: " + str(sso_loginCall.status_code))
        else:
            print("ERROR - PUT /sso/login (SSO User) Status Code: ")
            print(sso_loginCall.status_code)
            print(sso_loginCall.text)

        # POST /sso/logout
        time.sleep(1)
        sso_logout_headers = {'Authorization': sso_register_access_token}
        sso_logout_payload = {"clientId": client_id, "accessToken": sso_register_access_token}
        sso_logoutCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/logout', headers=sso_logout_headers, json=sso_logout_payload)
        if sso_logoutCall.status_code == 200:
            print("PUT /sso/logout (SSO User) Status Code: " + str(sso_logoutCall.status_code))
        else:
            print("ERROR - PUT /sso/logout (SSO User) Status Code: ")
            print(sso_logoutCall.status_code)
            print(sso_logoutCall.text)

        # POST /sso/email-exists-check (SSO user)
        time.sleep(1)
        email_exists_payload = {"email": testemailSSO, "clientId": client_id}
        emailExistsCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/email-exists-check',
                                        json=email_exists_payload)
        if emailExistsCall.status_code == 200:
            print("POST /sso/email-exists-check (SSO user) Status Code: " + str(emailExistsCall.status_code))
        else:
            print("ERROR - POST /sso/email-exists-check (SSO user) Status Code: ")
            print(emailExistsCall.status_code)
            print(emailExistsCall.text)

        # POST /sso/reset-password (SSO user)
        time.sleep(1)
        reset_password_headers = {'Authorization': sso_register_access_token}
        reset_password_payload = {"email": testemailSSO, "clientId": client_id}
        resetPasswordCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/reset-password', headers=reset_password_headers,
                                          json=reset_password_payload)
        if resetPasswordCall.status_code == 200:
            print("POST /sso/reset-password (SSO user) Status Code: " + str(resetPasswordCall.status_code))
        else:
            print("ERROR - POST /sso/reset-password (SSO user) Status Code: ")
            print(resetPasswordCall.status_code)
            print(resetPasswordCall.text)

        # POST /sso/register (Mobile user)
        time.sleep(1)
        mobile_register_payload = {'clientId': m_client_id, 'email': testemailMOB, 'password': var.CREDSapi.mobilePW, 'firstName': var.CREDSapi.mobileFName, 'lastName': var.CREDSapi.mobileLName, 'phone': var.CREDSapi.mobilePhone}
        mobile_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register',
                                         json=mobile_register_payload)
        if mobile_registerCall.status_code == 200:
            print('POST /sso/register (Mobile Registration) Status Code: ' + str(mobile_registerCall.status_code))
        else:
            print("ERROR - POST /sso/register (Mobile Registration) Status Code: ")
            print(mobile_registerCall.status_code)
            print(mobile_registerCall.text)

        # [Documentation - detail] grabbing the accessToken and refreshToken from the registration response body for use in later api calls
        mobile_registerResponse = []
        quoted = re.compile('"(.*?)"')
        for value in quoted.findall(sso_registerCall.text):
            # print(value)
            mobile_registerResponse.append(value)
        mobile_register_access_token = mobile_registerResponse[2]
        # For debugging token issues
        # print(mobile_registerCall.text)
        # print(mobile_register_access_token)

        # GET /promotions (Mobile user)
        time.sleep(1)
        promotions_headers = {'x-api-key': m_x_api_key}
        promotionsCall = requests.get('https://api-' + self.env + '.nylservices.net/promotions',
                                      headers=promotions_headers)
        if promotionsCall.status_code == 200:
            print("GET /promotions (Mobile user) Status Code: " + str(promotionsCall.status_code))
        else:
            print("ERROR - GET /promotions (Mobile user) Status Code: ")
            print(promotionsCall.status_code)
            print(promotionsCall.text)

        # GET /retailers/all (Mobile user)
        time.sleep(1)
        retailers_headers = {'x-api-key': m_x_api_key}
        retailersAllCall = requests.get('https://api-' + self.env + '.nylservices.net/retailers/all',
                                        headers=retailers_headers)
        if retailersAllCall.status_code == 200:
            print("GET /retailers/all (Mobile user) Status Code: " + str(retailersAllCall.status_code))
        else:
            print("ERROR - GET /retailers/all (Mobile user) Status Code: ")
            print(retailersAllCall.status_code)
            print(retailersAllCall.text)

        # POST /sso/login (Mobile user)
        time.sleep(1)
        mobile_login_payload = {"email": testemailMOB, "clientId": m_client_id, "password": var.CREDSapi.mobilePW}
        mobile_loginCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/login', json=mobile_login_payload)
        if mobile_loginCall.status_code == 200:
            print('POST /sso/login (Mobile user) Status Code: ' + str(mobile_loginCall.status_code))
        else:
            print("ERROR - POST /sso/login (Mobile user) Status Code: ")
            print(mobile_loginCall.status_code)
            print(mobile_loginCall.text)

        # GET /preferences (Mobile user)
        time.sleep(1)
        preferences_headers = {'x-api-key': m_x_api_key, 'Authorization': mobile_register_access_token}
        params = {'type': 'app'}
        preferencesGetCall = requests.get('https://api-' + self.env + '.nylservices.net/preferences', headers=preferences_headers, params=params)
        if preferencesGetCall.status_code == 200:
            print("GET /preferences (Mobile user) Status Code: " + str(preferencesGetCall.status_code))
        else:
            print("ERROR - GET /preferences (Mobile user) Status Code: ")
            print(preferencesGetCall.status_code)
            print(preferencesGetCall.text)

        # POST /preferences (Mobile user)
        time.sleep(1)
        preferences_headers = {'Authorization': mobile_register_access_token, 'x-api-key': m_x_api_key, 'Fcm-token': m_fcm_token}
        params = {'type': 'app'}
        preferences_payload = {"myGames": ["lotto", "megamillions"], "notifications": {"lotto": {"dayOfDrawing": "true", "minimumJackpot": "2500000"}}, "draws": {"lotto": [[1, 8, 72, 2, 1], [2, 8, 72, 2, 1], [3, 8, 72, 2, 1], [4, 8, 72, 2, 1]], "cash4life": [[1, 8, 72, 2, 1], [2, 8, 72, 2, 1], [3, 8, 72, 2, 1], [4, 8, 72, 2, 1]]}, "quickdraw": {"theme": 1}}
        preferencesPostCall = requests.post('https://api-' + self.env + '.nylservices.net/preferences', headers=preferences_headers, params=params, json=preferences_payload)
        if preferencesPostCall.status_code == 200:
            print("POST /preferences (Mobile user) Status Code: " + str(preferencesPostCall.status_code))
        else:
            print("ERROR - POST /preferences (Mobile user) Status Code: ")
            print(preferencesPostCall.status_code)
            print(preferencesPostCall.text)

        # GET /mobile-static-views/:pageid
        time.sleep(1)
        pages = ["settings-page", "visit-customer-service-center", "conditions", "privacy-policy", "contact-us", "faq-page", "ticket-purchase-policy", "faq-how-often-winning-numbers-updated", "faq-other-sources-winning-numbers", "faq-accurate-information", "faq-where-claim-prize", "faq-how-long-tickets-valid", "faq-connection-use-app", "faq-how-get-quick-draw-results", "faq-how-often-quick-draw-drawings", "faq-trouble-seeing-results", "faq-draw-times-games", "list-view-no-retailers-found", "mega-millions-how-to-play", "powerball-how-to-play", "lotto-how-to-play", "cash4life-how-to-play", "take-5-how-to-play", "numbers-how-to-play", "win-4-how-to-play", "quick-draw-how-to-play", "pick-10-how-to-play"]
        pages_headers = {'x-api-key': m_x_api_key}
        pagePassedFlags = []
        pageFailedFlags = []
        pageFailedStatusCode = []
        pageFailedList = []
        for page in pages:
            time.sleep(2)
            indiPageCall = requests.get('https://api-' + self.env + '.nylservices.net//mobile-static-views/' + page, headers=pages_headers)
            if indiPageCall.status_code == 200:
                pagePassedFlags.append(page)
            else:
                pagePassedFlags.append('xfail')
                pageFailedFlags.append(page)
                pageFailedStatusCode.append(indiPageCall.status_code)
        for f, s in zip(pageFailedFlags, pageFailedStatusCode):
            pageFailedList.append([(f, s)])

        if pageFailedList != []:
            print("ERROR - These individual GET /mobile-static-views/:pageid endpoints and their status codes:")
            print(pageFailedList)
        else:
            # print(pagePassedFlags)
            print("PASS - ALL individual GET /mobile-static-views/:pageid endpoints received Status Code: 200 ")

        print('\n***WARNING***\nBelow requests may fail due to IGT test environment availability')
        print('POST /ticket-scan/inquiry')
        print('GET /games/all/draws')
        print('GET /games/{game-name}/draws')
        print('Review IGT status for CAT and SQA here if failures are observed')
        info_headers = {'x-api-key': m_x_api_key}
        infoCall = requests.get('https://api-' + self.env + '.nylservices.net/info', headers=info_headers)
        print(infoCall.text)
        print('***WARNING*** \n')

        # GET /ticket-scan/count (Mobile user)
        time.sleep(1)
        ticketscan_count_headers = {'Authorization': mobile_register_access_token, 'x-api-key': m_x_api_key}
        ticketscanCountCall = requests.get('https://api-' + self.env + '.nylservices.net/ticket-scan/count', headers=ticketscan_count_headers)
        if ticketscanCountCall.status_code == 200:
            print("GET /ticket-scan/count Status Code: " + str(ticketscanCountCall.status_code))
        else:
            print("ERROR - GET /ticket-scan/count Status Code: ")
            print(ticketscanCountCall.status_code)
            print(ticketscanCountCall.text)

        # POST /ticket-scan/inquiry (Mobile user)
        time.sleep(1)
        ticketscan_inquiry_payload = {"barcodeData": "87600275207207466326295006"}
        ticketscan_inquiry_headers = {'Authorization': mobile_register_access_token, 'x-api-key': m_x_api_key}
        ticketscanInquiryCall = requests.post('https://api-' + self.env + '.nylservices.net/ticket-scan/inquiry', headers=ticketscan_inquiry_headers, json=ticketscan_inquiry_payload)
        if ticketscanInquiryCall.status_code == 200:
            print("POST /ticket-scan/inquiry Status Code: " + str(ticketscanInquiryCall.status_code))
        else:
            print("ERROR - GET /ticket-scan/inquiry Status Code: ")
            print(ticketscanInquiryCall.status_code)
            print(ticketscanInquiryCall.text)

        # GET /games/all/draws
        time.sleep(1)
        games_alldraws_headers = {'x-api-key': m_x_api_key}
        gamesAllDrawsCall = requests.get('https://api-' + self.env + '.nylservices.net/games/all/draws', headers=games_alldraws_headers)
        if gamesAllDrawsCall.status_code == 200:
            print("GET /games/all/draws Status Code: " + str(gamesAllDrawsCall.status_code))
        else:
            print("ERROR - GET /games/all/draws Status Code: ")
            print(gamesAllDrawsCall.status_code)
            print(gamesAllDrawsCall.text)

        # GET /games/{game-name}/draws
        time.sleep(1)
        games = ["megamillions", "powerball", "lotto", "cash4life", "take5", "numbers", "win4", "quickdraw", "pick10"]
        headers = {'x-api-key': m_x_api_key}
        gamePassedFlags = []
        gameFailedFlags = []
        gameFailedStatusCode = []
        gameFailedList = []
        for game in games:
            time.sleep(2)
            indiGameCall = requests.get('https://api-' + self.env + '.nylservices.net/games/' + game + '/draws', headers=headers)
            if indiGameCall.status_code == 200:
                gamePassedFlags.append(game)
            else:
                gamePassedFlags.append('xfail')
                gameFailedFlags.append(game)
                gameFailedStatusCode.append(indiGameCall.status_code)
        for f, s in zip(gameFailedFlags, gameFailedStatusCode):
            gameFailedList.append([(f, s)])

        if gameFailedList != []:
            print("ERROR - These individual GET /games/{game-name}/draws endpoints and their status codes:")
            print(gameFailedList)
        else:
            # print(gamePassedFlags)
            print("PASS - ALL individual GET /games/{game-name}/draws endpoints received Status Code: 200 ")

        # POST /sso/logout (Mobile user)
        time.sleep(1)
        mobile_logout_headers = {'Authorization': mobile_register_access_token}
        mobile_logout_payload = {"clientId": m_client_id, "accessToken": mobile_register_access_token}
        mobile_logoutCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/logout', headers=mobile_logout_headers, json=mobile_logout_payload)
        if mobile_logoutCall.status_code == 200:
            print('POST /sso/logout (Mobile user) Status Code: ' + str(mobile_logoutCall.status_code))
        else:
            print("ERROR - POST /sso/logout (Mobile user) Status Code: ")
            print(mobile_logoutCall.status_code)
            print(mobile_logoutCall.text)
            print('\n')

        # TODO Need to get correct headers and payload for the following endpoints
        # TODO POST /sso/confirm-reset-password
        # TODO GET /sso/email-confirmation-resend
        # TODO POST /sso/verify-jwt
        # TODO PATCH /users
        # TODO All Admin Console endpoints

        # Clean up - clear test user from userpool
        # Check for existing test SSO user and wipe it from userpool prior to register api call
        try:
            nylAdminDash.funct.purgeSSO(self, testemailSSO)
            print('test user ' + testemailSSO + ' purged \n')
        except:
            print('no test user ' + testemailSSO + ' found \n')
        # Check for existing test Mobile user and wipe it from userpool prior to register api call
        try:
            funct.purgeMobile(self, testemailMOB)
            print('test user ' + testemailMOB + ' purged \n')
        except:
            print('no test user ' + testemailMOB + ' found \n')

# use "report" variable in conftest.py to change report style on runner
if __name__ == "__main__":
    if confTest.NYLservicesBASE.report == "terminal":
        unittest.main(warnings='ignore')
    elif confTest.NYLservicesBASE.report == "html":
        unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='<html_report_dir>'))