from selenium import webdriver  # webdriver module provides all WebDriver implementations
import warnings
import unittest, time, re  # unittest is the testing framework, provides module for organizing test cases
import requests, json           # Requests provides ability to hit API Json provides ability to encode & decode Json files
import var, funct, confTest     # Custom class for NYL


class NYLServices(confTest.NYLservicesBASE):

    def test_apiStatusCode(self):
        # [Documentation - Summary] Checks that response status code 200 is returned
        # for Nylservices APIs with proper payloads in requests
        # For use with Entry Info file version: nyl06102020.txt

        testenv = self.env
        testemail = self.testemail
        # this email should not exist in the user pool
        # testemail2 = 'marie.liao+reg@rosedigital.co'
        # grabbing entry info through localized var/ funct files
        if testenv == 'dev':
            x_api_key = var.CREDSapi.devXKEY
            client_id = var.CREDSapi.devCID
        elif testenv == 'qa':
            x_api_key = var.CREDSapi.qaXKEY
            client_id = var.CREDSapi.qaCID
        elif testenv == 'stage':
            x_api_key = var.CREDSapi.stageXKEY
            client_id = var.CREDSapi.stageCID

        # Check for existing test user and wipe it from userpool prior to register api call
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')

        # [Documentation - detail] setting up an api call using the requests method
        # [Documentation - detail] setting headers to let api know that we have proper permissions to run api call
        # [Documentation - detail] setting payload in json body in the api call

        # POST /sso/register-verify (SSO User)
        sso_register_payload = {'clientId': client_id, 'email': testemail, 'password': var.CREDSapi.password,
                                'firstName': var.CREDSapi.fname, 'lastName': var.CREDSapi.lname,
                                'phone': var.CREDSapi.pnum,
                                'birthdate': var.CREDSapi.dob_month + "/" + var.CREDSapi.dob_date + "/" + var.CREDSapi.dob_year,
                                'streetNumber': var.CREDSapi.hnum, 'street': var.CREDSapi.street,
                                'city': var.CREDSapi.city, 'state': var.CREDSapi.state,
                                'zip': var.CREDSapi.zip}
        sso_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                         json=sso_register_payload)
        sso_register_access_token = str(sso_registerCall.text[24:1026])
        sso_register_refresh_token = str(sso_registerCall.text[1082:2866])
        # print("SSO Register Session AccessToken: " + sso_register_access_token)
        # print("SSO Register Session RefreshToken: " + sso_register_refresh_token)
        if sso_registerCall.status_code == 200:
            print("POST sso/register-verify Status Code: " + str(sso_registerCall.status_code))
        else:
            print("ERROR - POST sso/register-verify Status Code: ")
            print(sso_registerCall.status_code)
            print(sso_registerCall.text)

        # PUT /sso/register-verify (Profile Update)
        profile_update_headers = {'Authorization': sso_register_access_token}
        profile_update_payload = {'profileUpdate': {"verify": "true", "firstName": "firstname", "lastName": "lastName", "phone": "5182213991",
                              "birthdate": "01/12/1978", "streetNumber": "234", "street": "Dean", "city": "Brooklyn",
                              "state": "NY", "zip": "11217"}}
        sso_profileUpdateCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify',
                                              headers=profile_update_headers, json=profile_update_payload)
        if sso_profileUpdateCall.status_code == 200:
            print("PUT sso/register-verify (Profile Update) Status Code: " + str(sso_profileUpdateCall.status_code))
        else:
            print("ERROR - POST sso/register-verify Status Code: ")
            print(sso_profileUpdateCall.status_code)
            print(sso_profileUpdateCall.text)

        # PUT /sso/register-verify (SSN Confirmation)
        ssn_confirm_payload = {"ssnConfirmation": {"ssn": "1111"}}
        ssn_confirm_headers = {'Authorization': sso_register_access_token}
        ssnConfirmCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify', headers=ssn_confirm_headers,
                                 json=ssn_confirm_payload)
        if ssnConfirmCall.status_code == 200:
            print("PUT /sso/register-verify (SSN Confirmation) Status Code: " + str(ssnConfirmCall.status_code))
        else:
            print("ERROR - PUT sso/register-verify (SSN Confirmation) Status Code: ")
            print(ssnConfirmCall.status_code)
            print(ssnConfirmCall.text)

        # PUT /sso/register-verify (Phone Confirmation)
        phone_confirm_payload = {"ssnConfirmation": {"ssn": "1111"}}
        phone_confirm_headers = {'Authorization': sso_register_access_token}
        phoneConfirmCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/register-verify', headers=phone_confirm_headers,
                                 json=phone_confirm_payload)
        if phoneConfirmCall.status_code == 200:
            print("PUT /sso/register-verify (Phone Confirmation) Status Code: " + str(phoneConfirmCall.status_code))
        else:
            print("ERROR - PUT sso/register-verify (Phone Confirmation) Status Code: ")
            print(phoneConfirmCall.status_code)
            print(phoneConfirmCall.text)

        # PUT /sso/handle-govid-response
        handle_govid_payload = {"code": "qE4Dm5gm_PXrg20ul2phH7hYjWUj_OsbW1kMdLTRF_M", "govIdType": "usdl-desktop"}
        handle_govid_headers = {'Authorization': sso_register_access_token}
        handleGovidCall = requests.put('https://api-' + self.env + '.nylservices.net/sso/handle-govid-response', headers=handle_govid_headers,
                                 json=handle_govid_payload)
        if handleGovidCall.status_code == 200:
            print("PUT /sso/handle-govid-response Status Code: " + str(handleGovidCall.status_code))
        else:
            print("ERROR - PUT /sso/handle-govid-response Status Code: ")
            print(handleGovidCall.status_code)
            print(handleGovidCall.text)

        # TODO POST /sso/register (Used by Mobile)

        # POST /sso/login
        sso_login_payload = {"email": testemail, "clientId": client_id, "password": var.CREDSapi.password}
        sso_loginCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/login', json=sso_login_payload)
        sso_login_access_token = str(sso_loginCall.text[24:1026])
        sso_login_refresh_token = str(sso_loginCall.text[1082:2866])
        # print("SSO Login Session AccessToken: " + sso_login_access_token)
        # print("SSO Login Session RefreshToken: " + sso_login_refresh_token)
        if sso_loginCall.status_code == 200:
            print("PUT /sso/login (SSO User) Status Code: " + str(sso_loginCall.status_code))
        else:
            print("ERROR - PUT sso/login (SSO User Status Code: ")
            print(sso_loginCall.status_code)
            print(sso_loginCall.text)

        # TODO POST /sso/login (Mobile User) Need to get correct headers and payload
        # mob_login_payload = {"email": var.CREDSapi.mobileUN, "clientId": client_id, "password": var.CREDSapi.mobilePW}
        # mob_loginCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/login', json=mob_login_payload)
        # mob_login_access_token = str(sso_loginCall.text[24:1026])
        # print("Mobile Session Access Token: ")
        # print(mob_login_access_token)
        # print("sso/login (Mobile User) Status Code: ")
        # print(mob_loginCall.status_code)

        # TODO POST /sso/confirm-reset-password Need to get correct headers and payload
        # confirm_reset_payload = {}
        # confirm_reset_headers = {'Authorization': sso_register_access_token}
        # confirmResetCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/confirm-reset-password', headers=confirm_reset_headers,
        #                                 json=confirm_reset_payload)
        # print("POST sso/confirm-reset-password Status Code: " + str(confirmResetCall.status_code))
        # if confirmResetCall.status_code == 200:
        #     print("POST /sso/confirm-reset-password Status Code: " + str(confirmResetCall.status_code))
        # else:
        #     print("ERROR - POST /sso/confirm-reset-password Status Code: ")
        #     print(confirmResetCall.status_code)
        #     print(confirmResetCall.text)

        # TODO GET /sso/email-confirmation-resend
        # email_confirm_payload = {"email": testemail, "clientId": client_id}
        # email_confirm_headers = {'Authorization': sso_register_access_token}
        # emailConfirmCall = requests.get('https://api-' + self.env + '.nylservices.net/sso/email-confirmation-resend', headers=email_confirm_headers,
        #                                 json=email_confirm_payload)
        # if emailConfirmCall.status_code == 200:
        #     print("GET /sso/email-confirmation-resend Status Code: " + str(emailConfirmCall.status_code))
        # else:
        #     print("GET /sso/email-confirmation-resend Status Code: ")
        #     print(emailConfirmCall.status_code)
        #     print(emailConfirmCall.text)

        # POST /sso/email-exists-check
        email_exists_payload = {"email": testemail, "clientId": client_id}
        emailExistsCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/email-exists-check',
                                        json=email_exists_payload)
        if emailExistsCall.status_code == 200:
            print("POST sso/email-exists-check Status Code: " + str(emailExistsCall.status_code))
        else:
            print("ERROR - POST sso/email-exists-check Status Code: ")
            print(emailExistsCall.status_code)
            print(emailExistsCall.text)

        # POST /sso/phone-code-gen
        phone_gen_payload = {"type": "sms"}
        phone_gen_headers = {'Authorization': sso_login_access_token}
        phoneGenCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/phone-code-gen', headers=phone_gen_headers,
                                 json=phone_gen_payload)
        if phoneGenCall.status_code == 200:
            print("POST sso/phone-code-gen Status Code: " + str(phoneGenCall.status_code))
        else:
            print("ERROR - POST sso/phone-code-gen Status Code: ")
            print(phoneGenCall.status_code)
            print(phoneGenCall.text)

        # POST /sso/refresh-token
        refresh_token_payload = {"clientId": client_id, "refreshToken": sso_login_refresh_token}
        refresh_token_headers = {'x-api-key': x_api_key}
        refreshTokenCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/refresh-token', headers=refresh_token_headers,
                                        json=refresh_token_payload)
        if refreshTokenCall.status_code == 200:
            print("POST /sso/refresh-token Status Code: " + str(refreshTokenCall.status_code))
        else:
            print("ERROR - POST /sso/refresh-token Status Code: ")
            print(refreshTokenCall.status_code)
            print(refreshTokenCall.text)

        # POST /sso/reset-password
        reset_password_payload = {"email": testemail, "clientId": client_id}
        reset_password_headers = {'Authorization': sso_login_access_token}
        resetPasswordCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/reset-password', headers=reset_password_headers,
                                          json=reset_password_payload)
        if resetPasswordCall.status_code == 200:
            print("POST /sso/reset-password Status Code: " + str(resetPasswordCall.status_code))
        else:
            print("ERROR - POST /sso/reset-password Status Code: ")
            print(resetPasswordCall.status_code)
            print(resetPasswordCall.text)

        # TODO POST /sso/verify-jwt

        # GET /retailers/all
        retailers_headers = {'x-api-key': x_api_key}
        retailersAllCall = requests.get('https://api-' + self.env + '.nylservices.net/retailers/all', headers=retailers_headers)
        if retailersAllCall.status_code == 200:
            print("GET /retailers/all Status Code: " + str(retailersAllCall.status_code))
        else:
            print("ERROR - GET /retailers/all Status Code: ")
            print(retailersAllCall.status_code)
            print(retailersAllCall.text)

        # TODO GET /ticket-scan/count Need to get correct headers and payload for mobile user access
        # ticketscan_count_headers = {'Authorization': mob_access_token, 'x-api-key': x_api_key}
        # ticketscanCountCall = requests.get('https://api-' + self.env + '.nylservices.net/ticket-scan/count', headers=ticketscan_count_headers)
        # if ticketscanCountCall.status_code == 200:
        #     print("GET /ticket-scan/count Status Code: " + str(ticketscanCountCall.status_code))
        # else:
        #     print("ERROR - GET /ticket-scan/count Status Code: ")
        #     print(ticketscanCountCall.status_code)
        #     print(ticketscanCountCall.text)

        # TODO POST /ticket-scan/inquiry Need to get correct headers and payload for mobile user access
        # ticketscan_inquiry_payload = {"barcodeData": "87500250900538108490920102"}
        # headers = {'Authorization': mob_access_token, 'x-api-key': x_api_key}
        # ticketscanInquiryCall = requests.post('https://api-' + self.env + '.nylservices.net/ticket-scan/inquiry', ticketscan_inquiry_headers=headers, json=ticketscan_inquiry_payload)
        # if ticketscanCountCall.status_code == 200:
        #     print("POST /ticket-scan/inquiry Status Code: " + str(ticketscanInquiryCall.status_code))
        # else:
        #     print("ERROR - GET /ticket-scan/count Status Code: ")
        #     print(ticketscanInquiryCall.status_code)
        #     print(ticketscanInquiryCall.text)

        # GET /games/{game-name}/draws
        games = ["megamillions", "powerball", "lotto", "cash4life", "take5", "numbers", "win4", "quickdraw", "pick10"]
        headers = {'x-api-key': x_api_key}
        gamePassedFlags = []
        gameFailedFlags = []
        gameFailedStatusCode = []
        gameFailedList = []
        for game in games:
            indiGameCall = requests.get('https://api-' + self.env + '.nylservices.net/games/' + game + '/draws', headers=headers)
            if indiGameCall.status_code == 200:
                gamePassedFlags.append(game)
            else:
                gamePassedFlags.append('xfail')
                gameFailedFlags.append(game)
                gameFailedStatusCode.append(indiGameCall.status_code)
        for f, s in zip(gameFailedFlags, gameFailedStatusCode):
            gameFailedList.append([(f, s)])

        print("Pass - Individual Games endpoints: ")
        print(gamePassedFlags)
        print("FAIL - Individual Games endpoints and their status codes:")
        print(gameFailedFlags)

        # GET /games/all/draws
        games_alldraws_headers = {'x-api-key': x_api_key}
        gamesAllDrawsCall = requests.get('https://api-' + self.env + '.nylservices.net/games/all/draws', headers=games_alldraws_headers)
        if gamesAllDrawsCall.status_code == 200:
            print("GET /games/all/draws Status Code: " + str(gamesAllDrawsCall.status_code))
        else:
            print("ERROR - GET /games/all/draws Status Code: ")
            print(gamesAllDrawsCall.status_code)
            print(gamesAllDrawsCall.text)

        # TODO GET /preferences Need to get correct headers and payload for mobile user access
        # preferences_headers = {'Authorization': mob_access_token, 'x-api-key': x_api_key}
        # params = {'type': 'app'}
        # preferencesGetCall = requests.get('https://api-' + self.env + '.nylservices.net/preferences', headers=preferences_headers, params=params)
        # if preferencesGetCall.status_code == 200:
        #     print("GET /preferences Status Code: " + str(preferencesGetCall.status_code))
        # else:
        #     print("ERROR - GET /preferences Status Code: ")
        #     print(preferencesGetCall.status_code)
        #     print(preferencesGetCall.text)

        # TODO POST /preferences Need to get correct headers and payload for mobile user access
        # preferences_headers = {'Authorization': mob_access_token, 'x-api-key': x_api_key, 'Fcm-token': fcm_token}
        # params = {'type': 'app'}
        # payload = {}
        # preferencesPostCall = requests.post('https://api-' + self.env + '.nylservices.net/preferences', headers=preferences_headers, params=params, payload=payload)
        # if preferencesPostCall.status_code == 200:
        #     print("POST /preferences Status Code: " + str(preferencesPostCall.status_code))
        # else:
        #     print("ERROR - POST /preferences Status Code: ")
        #     print(preferencesPostCall.status_code)
        #     print(preferencesPostCall.text)

        # GET /promotions
        promotions_headers = {'x-api-key': x_api_key}
        promotionsCall = requests.get('https://api-' + self.env + '.nylservices.net/promotions', headers=promotions_headers)
        if promotionsCall.status_code == 200:
            print("GET /promotions Status Code: " + str(promotionsCall.status_code))
        else:
            print("ERROR - GET /promotions Status Code: ")
            print(promotionsCall.status_code)
            print(promotionsCall.text)

        # GET /users
        users_headers = {'Authorization': sso_login_access_token}
        usersGetCall = requests.get('https://api-' + self.env + '.nylservices.net/users', headers=users_headers)
        if promotionsCall.status_code == 200:
            print("GET /users Status Code: " + str(usersGetCall.status_code))
        else:
            print("ERROR - GET /users Status Code: ")
            print(usersGetCall.status_code)
            print(usersGetCall.text)

        # TODO PATCH /users Need correct headers and payloads
        # headers = {'Authorization': sso_login_access_token}
        # usersPatchCall = requests.patch('https://api-' + self.env + '.nylservices.net/users', headers=headers)
        # if usersPatchCall.status_code == 200:
        #     print("PATCH /users Status Code: " + str(usersPatchCall.status_code))
        # else:
        #     print("ERROR - PATCH /users Status Code: ")
        #     print(usersPatchCall.status_code)
        #     print(usersPatchCall.text)

        # Clean up - clear test user from userpool
        try:
            funct.purge(self, testemail)
            print('test user purged')
        except:
            print('no test user found')

        # # TODO Work in Progress
        # # Below code would run through the endpoints in a for loop,
        # # passing the necessary information needed in headers and payloads
        #
        # testenv = self.env
        # testemail = self.testemail
        # # this email should not exist in the user pool
        # # testemail2 = 'marie.liao+reg@rosedigital.co'
        # # grabbing entry info through localized var/ funct files
        # if testenv == 'dev':
        #     x_api_key = var.CREDSapi.devXKEY
        #     client_id = var.CREDSapi.devCID
        # elif testenv == 'qa':
        #     x_api_key = var.CREDSapi.qaXKEY
        #     client_id = var.CREDSapi.qaCID
        # elif testenv == 'stage':
        #     x_api_key = var.CREDSapi.stageXKEY
        #     client_id = var.CREDSapi.stageCID
        #
        # # Check for existing test user and wipe it from userpool prior to register api call
        # try:
        #     funct.purge(self, testemail)
        #     print('test user purged')
        # except:
        #     print('no test user found')
        #
        # ssoEndpoints = ["register-verify", "handle-govid-response", "register", "login", "logout", "confirm-reset-password", "email-confirmation-resend", "email-exists-check", "phone-code-gen", "refresh-token", "reset-password", "verify-jwt"]
        # retailersEndpoints = ["all"]
        # ticketscanEndpoints = ["count", "inquiry"]
        # gamesEndpoints = ["{game-name}/draws", "all/draws"]
        # preferencesEndpoints = ["preferences"]
        # promotionsEndpoints = ["promotions"]
        # usersEndpoints = ["users"]
        # adminEndpoints = ["users", "users/:userID/verify", ]
        #
        # # [Documentation - detail] POST /sso/register-verify & POST /sso/login have to run first
        # # to set the token variables for the remaining calls in the for loop
        # sso_register_payload = {'clientId': client_id, 'email': testemail, 'password': var.CREDSapi.password,
        #                         'firstName': var.CREDSapi.fname, 'lastName': var.CREDSapi.lname,
        #                         'phone': var.CREDSapi.pnum,
        #                         'birthdate': var.CREDSapi.dob_month + "/" + var.CREDSapi.dob_date + "/" + var.CREDSapi.dob_year,
        #                         'streetNumber': var.CREDSapi.hnum, 'street': var.CREDSapi.street,
        #                         'city': var.CREDSapi.city, 'state': var.CREDSapi.state,
        #                         'zip': var.CREDSapi.zip}
        # sso_registerCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/register-verify',
        #                                  json=sso_register_payload)
        # sso_register_access_token = str(sso_registerCall.text[24:1026])
        # sso_register_refresh_token = str(sso_registerCall.text[1082:2866])
        # print("SSO Register Session Access Token: ")
        # print(sso_register_access_token)
        # if sso_registerCall.status_code == 200:
        #     print("POST sso/register-verify Status Code: ")
        #     print(sso_registerCall.status_code)
        # else:
        #     print(sso_registerCall.text)
        #
        # sso_login_payload = {"email": testemail, "clientId": client_id, "password": var.CREDSapi.password}
        # sso_loginCall = requests.post('https://api-' + self.env + '.nylservices.net/sso/login', json=sso_login_payload)
        # sso_login_access_token = str(sso_loginCall.text[24:1026])
        # sso_login_refresh_token = str(sso_loginCall.text[1082:2866])
        # print(sso_login_refresh_token)
        # print("sso/login Status Code: ")
        # print(sso_loginCall.status_code)
        #
        # NYLServices.passedFlags = []
        # NYLServices.failedFlags = []
        # NYLServices.statusResponse = []
        #
        # methods = ["post", "post", "get", "get", "post", "get", "get"]
        # endpoints = ["sso/login", "email-exists-check", "sso/phone-code-gen", "sso/refresh-token", "sso/reset-password", "retailers/all", "ticket-scan/count"]
        # head = [(), (), ({'Authorization': access_token}), ({'x-api-key': x_api_key}), ({'Authorization': access_token}), ({'x-api-key': x_api_key}), ({'Authorization': access_token}, {'x-api-key': x_api_key})]
        # payloads = [login_payload, email_exists_payload, phone_gen_payload, refresh_token_payload, reset_password_payload, (), ()]
        #
        # for m, e, h, p in zip(methods, endpoints, heads, payloads):
        #     estring = str(e)
        #     if m == "post":
        #         apiCalls = requests.post('https://api-' + self.env + '.nylservices.net/ + estring, json=p)
        #         if apiCalls.status_code == 200:
        #             NYLServices.passedFlags.append(e)
        #         else:
        #             NYLServices.passedFlags.append('xfail')
        #             NYLServices.failedFlags.append(e)
        #             NYLServices.statusResponse.append(apiCalls.status_code)
        #     elif m == "get":
        #         apiCalls = requests.get('https://api-' + self.env + '.nylservices.net/ + estring, headers=h, json=p)
        #         if apiCalls.status_code == 200:
        #             NYLServices.passedFlags.append(e)
        #         else:
        #             NYLServices.passedFlags.append('xfail')
        #             NYLServices.failedFlags.append(e)
        #             NYLServices.statusResponse.append(apiCalls.status_code)
        #     elif m == "put":
        #         apiCalls = requests.put('https://api-' + self.env + '.nylservices.net/ + estring, headers=h, json=p)
        #         if apiCalls.status_code == 200:
        #             NYLServices.passedFlags.append(e)
        #         else:
        #             NYLServices.passedFlags.append('xfail')
        #             NYLServices.failedFlags.append(e)
        #             NYLServices.statusResponse.append(apiCalls.status_code)
        #     elif m == "patch":
        #         apiCalls = requests.patch('https://api-' + self.env + '.nylservices.net/ + estring, headers=h, json=p)
        #         if apiCalls.status_code == 200:
        #             NYLServices.passedFlags.append(e)
        #         else:
        #             NYLServices.passedFlags.append('xfail')
        #             NYLServices.failedFlags.append(e)
        #             NYLServices.statusResponse.append(apiCalls.status_code)
        #
        #
        # if len(NYLServices.failedFlags) > 0:
        #     print(NYLServices.passedFlags)
        #     print(NYLServices.failedFlags)
        #     print(NYLServices.statusResponse)
        #     #raise Exception("ERROR: above API calls failed!")
        #


# Boiler plate code to run the test suite
if __name__ == "__main__":
    # First runner will enable html logs on your current directory, second runner will keep local console logs
    unittest.main(warnings='ignore')
    # unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='html_report_dir'))
