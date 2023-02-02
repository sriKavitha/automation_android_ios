const HomePage = require('../../pages/android/home-page');
const LoginPage = require('../../pages/android/login-page')

describe('Android app user - Cannot login with invalid credentials', () => {
    it('Verify Error Icon and error message is displayed', async() => {
        
        // https://rosedigital.atlassian.net/browse/MRMNYL-191 - Manual testcase Jira ticket

         // 1. wait for the app till it is fully launched 
        await HomePage.threeButtons.waitForDisplayed();

        // 2. assert for the NYL LOGO and 3 buttons on the Home screen
        // CONTINUE AS A GUEST, LOG IN, CREATE ACCOUNT 3 buttons 
        const containerBtn = await HomePage.threeButtons;
        await expect(containerBtn).toBeDisplayed({message: "Home page should have NYL Logo and all the three buttons..."});
        
        // 3. click on LOG IN button
        await HomePage.loginBtnHomePage.click();

         // 4. verify the LOG IN text in Login page
         const loginTitleTxt = LoginPage.loginPage_TitleText;
         await expect(loginTitleTxt).toExist({message: "The title is missing in the Login Page "});
        //  await driver.pause(1000);

        // 5. login with invalid creds
         await LoginPage.login_invalidCreds("bad_appEmail@gmail.com","badpassword");

         // 6. assert the error message
        const elem = await LoginPage.invalid_eMailPasswordMessage;
        await elem.waitUntil(async function () {
            return (await elem.getText()) === 'Whoops! Incorrect email or password. Try again.'
        }, {
            timeoutMsg: 'Error message is not displayed....'
        });
        
        // 7. display user can't log in with invalid creds on console
        await console.log("\n\nNYL user cannot login due to the error message..", await LoginPage.invalid_eMailPasswordMessage.getText());
    });
});