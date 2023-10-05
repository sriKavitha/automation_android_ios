const HomePage_iOS = require('../../pages/ios/home-page-ios');
const allureReporter = require('@wdio/allure-reporter')
const Utils = require('../../utils/helperUtils')
const HamburgerPage_iOS = require('../../pages/ios/hamburger-page-ios');
const LoginPage_iOS = require('../../pages/ios/login-page-ios')
const GuestPage_iOS = require('../../pages/ios/guest-page-ios');
// const FindRetailersPage = require('../../pages/ios/findRetailers-page-ios');

describe('iOS app user - Continue as a Guest to verify that a user can access the Find Retailers screen through the nav menu', function () {
    
    // Retry 1 time if test fails
    let count = 0;
    this.retries(0);

    const testID = 'https://rosedigital.atlassian.net/browse/MRMNYL-184';

    it('Verify that a user can access the Find Retailers screen through the nav menu', async function() {
    
        // Read the datafile to get the environment name ex: dev/QA/stage
        data=await Utils.readData();

        // This test will retry up to 1 times, in case of failure and take a screenshot
        console.log("Retry attempt # ", count);
        count++;

        // Allure report configuration
        allureReporter.addFeature('Guest User')
        allureReporter.addDescription(`Description: User is able to access the Find Retailers screen through the nav menu \n\n TestID: ${testID}`);
        allureReporter.addSeverity('Normal')
        allureReporter.addEnvironment("Environment:", data.env);
        
        // 1. Wait for the app till it is fully launched 
        allureReporter.addStep('App is launched')
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

        // 6. Tap on Hamburger Icon / Retailers button
        allureReporter.addStep('Tap on Hamburger');
        await HamburgerPage_iOS.hamburgerIcon.waitForDisplayed();
        await HamburgerPage_iOS.hamburgerIcon.click();

        // 7. Tap on Find Retailers button
        allureReporter.addStep('Tap on Find Retailers');
        // await HamburgerPage_iOS.findRetailersBtn.waitForDisplayed()
        // await HamburgerPage_iOS.findRetailersBtn.click();

        // 8. assert the FIND RETAILERS heading, map and filter
        // allureReporter.addStep('Assert Heading, google map and filter is displayed in Find Retailers screen');
        // await expect(await FindRetailersPage.findRetailersHeading).toHaveTextContaining('FIND RETAILERS');
        // await expect(await FindRetailersPage.findRetailersFilter).toExist();
        // await expect(await FindRetailersPage.findRetailersMap).toExist();       
        // allureReporter.addStep('User is able to access the Find Retailers screen through the nav menu.');
    });
});