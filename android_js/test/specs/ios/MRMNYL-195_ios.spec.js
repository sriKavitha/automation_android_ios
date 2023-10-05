const HomePage_iOS = require('../../pages/ios/home-page-ios');
const GuestPage_iOS = require('../../pages/ios/guest-page-ios')
const HelperPage = require('../../utils/helperUtils');
//const HamburgerPage_iOS = require('../../pages/ios/hamburger-page-ios');
const MegaMillionsGamePage_iOS = require('../../pages/ios/megaMillionsGame-page-ios');
const allureReporter = require('@wdio/allure-reporter');
const Utils = require('../../utils/helperUtils')

describe('iOS app user - Continue as a Guest to login from Mega Millions Notifications', function () {

    // Retry 1 time if test fails
    let count =0;
    this.retries(0);
    
    it('Verify iOS user is able to log in from Mega Millions NOTIFICATION SETTINGS screen', async function() {

      // Read the datafile to get the environment name ex: dev/QA/stage
      data=await Utils.readData();

      // This test will retry up to 1 times, in case of failure and take a screenshot
      console.log('Retry attempt # ',count);
      count++;

      // allure report configuration
      allureReporter.addFeature('Guest User');
      allureReporter.addTestId('https://rosedigital.atlassian.net/browse/MRMNYL-195');
      allureReporter.addDescription('Description: User is able to login from Mega Millions NOTIFICATION SETTINGS screen');
      allureReporter.addSeverity('normal');
      allureReporter.addEnvironment("Environment:", data.env);
      
      // 1. wait for the app till it is fully launched 
      allureReporter.addStep('App is launched');
      await (await HomePage_iOS.threeButtons).waitForDisplayed();
      
      // 2. assert for the NYL LOGO and 3 buttons on the Home screen
      // CONTINUE AS A GUEST, LOG IN, CREATE ACCOUNT 3 buttons 
      const containerBtn = await HomePage_iOS.threeButtons;
      await expect(containerBtn).toBeDisplayed({message: "Home page should have NYL Logo and all the three buttons..."});

      // 3. tap on CONTINUE AS A GUEST
      allureReporter.addStep('Tap on CONTINUE AS A GUEST button');
      await HomePage_iOS.countinueGuestBtnHomePage.click();

      // 4. wait for intro cards are displayed and swipe right 
      const ele = await HomePage_iOS.intro
      await ele.waitForDisplayed({timeout:3000})
      await HelperPage.swipe_ios();

      //5. assert All Games tab
      await expect(GuestPage_iOS.allGamesTab).toExist({message: "All Games Tab is not found..."});

      //  6. tap on ALL GAMES
      allureReporter.addStep('Tap on ALL GAMES tab');
      await GuestPage_iOS.allGamesTab.click();
      await driver.pause(1000)

      // 7. Swipe until Mega Millions game appears and tap
      allureReporter.addStep('Swipe until Mega Millions game appears and tap');
      await MegaMillionsGamePage_iOS.megaMillionsGameScroll();

      // 8. Assert winning numbers, next drawing & current jackpot info
      allureReporter.addStep('Assert winning numbers, next drawing & current jackpot info');
      await expect(await MegaMillionsGamePage_iOS.mega_winningNumbersInfo).toExist();
      await expect(await MegaMillionsGamePage_iOS.mega_nextDrawCurrentJackpotInfo).toExist();

      // 9. Swipe until SET NOTIFICATIONS FOR THIS GAME button and tap on it
      allureReporter.addStep('Swipe down to see SET NOTIFICATIONS FOR THIS GAME button and tap on it');
      await MegaMillionsGamePage_iOS.mega_setNotifySwipe;
      await (await MegaMillionsGamePage_iOS.mega_setNotificationBtn).click();

      // 10. Login using valid credentials
      await MegaMillionsGamePage_iOS.megaMillions_Login();
      allureReporter.addStep('User is successfully signed in from Mega Millions NOTIFICATION SETTINGS screen');

      // 11. Display console message
      console.log("\nVerified successfully... Guest User is able to signin from Mega Millions NOTIFICATION SETTINGS screen...");
      
    });
});