const HomePage_iOS = require('../../pages/ios/home-page-ios');
const allureReporter = require('@wdio/allure-reporter')
const Utils = require('../../utils/helperUtils')
// const HamburgerPage = require('../../pages/android/hamburger-page');
// const HamburgerPage_iOS = require('../../pages/ios/hamburger-page-ios')
const LoginPage_iOS = require('../../pages/ios/login-page-ios')
const GuestPage_iOS = require('../../pages/ios/guest-page-ios');
const PromotionsPage_iOS = require('../../pages/ios/promotions-page-ios');

describe('iOS app user - Continue as a Guest to verify that a user can access the Promotions screen through the nav menu', function () {
    
    // Retry 1 time if test fails
    let count = 0;
    this.retries(0);
    
    const testID = 'https://rosedigital.atlassian.net/browse/MRMNYL-181';

    it('Verify that a user can access the Promotions screen through the nav menu', async function() {
    
        // Read the datafile to get the environment name ex: dev/QA/stage
        var data = await Utils.readData();

        // This test will retry up to 1 times, in case of failure and take a screenshot
        console.log("Retry attempt # ", count);
        count++;

        // Allure report configuration
        allureReporter.addFeature('Guest User');
        allureReporter.addDescription(`Description: User is able to access the Promotions screen through the nav menu \n\n TestID: ${testID}`);
        allureReporter.addSeverity('Normal');
        allureReporter.addEnvironment("Environment:", data.env);
        
        // 1. Wait for the app till it is fully launched 
        allureReporter.addStep('App is launched');
        await (await HomePage_iOS.threeButtons).waitForDisplayed();
        
        // 2. Assert for the NYL LOGO and 3 buttons on the Home screen
        // CONTINUE AS A GUEST, LOG IN, CREATE ACCOUNT 3 buttons 
        const containerBtn = await HomePage_iOS.threeButtons;
        await expect(containerBtn).toBeDisplayed({message: "Home page should have NYL Logo and all the three buttons..."});
        
        // 3. tap on CONTINUE AS A GUEST
        allureReporter.addStep('Tap on CONTINUE AS A GUEST button');
        await HomePage_iOS.countinueGuestBtnHomePage.click();

        // 4. wait for intro cards are displayed and swipe right 
        await (await LoginPage_iOS.loginPage_FullSectionImage).waitForDisplayed({timeout: 2000});
        await Utils.swipe_ios();

         //5. Assert All Games tab
        await expect(GuestPage_iOS.allGamesTab).toExist({message: "All Games Tab is not found..."});
        console.log("I finished...")

        // 6. Tap on Hamburger Icon
        allureReporter.addStep('Tap on Hamburger');
        // await HamburgerPage_iOS.hamburgerIcon.waitForDisplayed();
        // await HamburgerPage_iOS.hamburgerIcon.click();

        // 7. Tap on Promotions button
        await PromotionsPage_iOS.promotionsBtn.waitForDisplayed();
        await PromotionsPage_iOS.promotionsBtn.click();

        // 8. assert the Promotions heading
        await expect(await PromotionsPage_iOS.promotionsHeading).toHaveTextContaining('PROMOTIONS');
        // await expect(await PromotionsPage.promotionsTitle).toHaveTextContaining('New York Lottery Resumes');
        // await expect(await PromotionsPage.promotionsIcon).toExist();

        // 9. Display console message
        allureReporter.addStep('User is able to access the Promotions screen through the nav menu.');
        console.log("\nVerified successfully... User is able to access the Promotions screen through the nav menu.");        

    });
});
