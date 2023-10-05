const allureReporter = require('@wdio/allure-reporter');
const HomePage_iOS = require('../../pages/ios/home-page-ios')
const LoginPage = require('../../pages/ios/login-page-ios')
const Utils = require('../../utils/helperUtils')
describe('iOS app user - Login from NYL Home screen with valid credentials', function () {
    
    // Retry 1 time if test fails
    let count =0;
    this.retries(0);
    
    it('Verify NYL iOS app user can login into the account successfully', async function() {
        
        // Read the datafile to get the environment name ex: dev/QA/stage
        data=await Utils.readData();
        
        // This test will retry up to 1 times, in case of failure and take a screenshot
        console.log('Retry attempt # ',count);
        count++;

        // allure report configuration
        allureReporter.addFeature('Login');
        allureReporter.addTestId('https://rosedigital.atlassian.net/browse/MRMNYL-193');
        allureReporter.addDescription('Description: Description: Verify NYL user can login with valid credentials from NYL app');
        allureReporter.addSeverity('critical');
        allureReporter.addEnvironment("Environment:", data.env);

         // 1. Wait for the app till it is fully launched 
        allureReporter.addStep('App is launched');
        await HomePage_iOS.threeButtons.waitForDisplayed();

        // 2. Assert for the NYL LOGO and 3 buttons on the Home screen
        // CONTINUE AS A GUEST, LOG IN, CREATE ACCOUNT 3 buttons 
        const containerBtn = await HomePage_iOS.threeButtons;
        await expect(containerBtn).toBeDisplayed({message: "Home page should have NYL Logo and all the three buttons..."});
        
        // 3. Tap on LOG IN button
        allureReporter.addStep('Tap on LOGIN button');
        await HomePage_iOS.loginBtnHomePage.click();

        // 4. Verify the title LOG IN text in Login page
        const loginTitleTxt = await LoginPage.loginPage_TitleText;
        console.log("hello1",await loginTitleTxt.getText())
        await expect(loginTitleTxt).toExist({message: "The title is missing in the Login Page "});
        allureReporter.addStep('Verified the title LOG IN in Login page');


        // 5. Login with valid creds
        allureReporter.addStep('Key in valid credentials for Email and Password values');
        await LoginPage.login();
        await driver.pause(3000)

        // 6. Assert banner image is dispalyed after NYL user sign in
        const flag = await (LoginPage.loginPage_FullSectionImage).waitForDisplayed({timeout: 30000});
        console.log("flag:",flag)
        await expect(flag).toEqual(true, {message: "Banner image is not displayed after NYL user signed in...\n"});
        allureReporter.addStep('NYL user is successfully signed into NYL app using valid credentials');

        // 7. Display user is successfully signed in message on the console
        await console.log("\nNYL user is successfully signed in...\n\n");
    });
});