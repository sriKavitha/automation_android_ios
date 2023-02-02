const RegisterAccount = require('../../pages/android/registerAccount-page');
const GamesPage = require('../../pages/android/games-page');
const HomePage = require('../../pages/android/home-page');
const HelperPage = require('../../utils/helperUtils');
const AccountDetailsPage = require('../../pages/android/accountDetails-page');

describe('Android app user - Register an user from NYL Home screen successfully', () => {
    
    it('Verify NYL Android app user can register an account', async() => {
    
        // https://rosedigital.atlassian.net/browse/MRMNYL-204 - Manual testcase Jira ticket

        // 1. wait for the app till it is fully launched 
        await HomePage.threeButtons.waitForDisplayed();
        
        
        // 2. assert for the NYL LOGO and 3 buttons on the Home screen
        // CONTINUE AS A GUEST, LOG IN, CREATE ACCOUNT 3 buttons 
        const containerBtn = await HomePage.threeButtons;
        await expect(containerBtn).toBeDisplayed({message: "Home page should have NYL Logo and all the three buttons..."});
        
        // 3. click on CREATE ACCOUNT button
        await HomePage.createAccountHome.click();
        
        // 4. keyin the values for all required fields
        const registrationDetails = await RegisterAccount.submitRegistrationForm();
        
        // 5. assert the registration is successful
        await expect(RegisterAccount.hourSymbol).toExist({message: "Registration is not successfull..."});
        await HelperPage.swipe();

        // 6. assert user landed into Games Page
        await expect(GamesPage.gamesTxt).toHaveTextContaining("GAMES");

        // 7. goTo Settings page
        await GamesPage.settings_Page();

        // 8. get Account Details
        const acctDetails = await AccountDetailsPage.getAccountDeatils();
        
        // 9. assert registration details matches with account deatils from app
        await expect(registrationDetails).toEqual(acctDetails); 

        // 10. display user is successfully registered message on the console
        await console.log("\nYour registration is successfully completed... Please check your email. ", registrationDetails[2]);
        await console.log("\nregistration user",registrationDetails);
        await console.log("\naccount details",acctDetails);
        
    });
});