const Utils = require('../../utils/helperUtils');
class LoginPage_iOS {

    get loginPage_TitleText()
    {
        return $('(//XCUIElementTypeStaticText[@name="LOG IN"])[1]');
    }

    get loginPage_Email()
    {
        return $('//XCUIElementTypeTextField[@value="Email"]');
    }

    get loginPage_Password()
    {
        return $('//XCUIElementTypeSecureTextField[@value="Password"]');
    }

    get loginPage_LoginBtn()
    {
        return $('(//XCUIElementTypeStaticText[@name="LOG IN"])[2]');
    }

    get loginPage_FullSectionImage()
    {
        // const introPage = "**/XCUIElementTypeWindow[3]/XCUIElementTypeOther";
        // return $(`-ios class chain:${introPage}`);
        // return $('//XCUIElementTypeApplication[contains(@name,"Official NY Lottery")]/XCUIElementTypeWindow[3]/XCUIElementTypeOther')
        const introScr = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        return $(`-ios class chain:${introScr}`)
    }
    get intro()
    {
        const introScr = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        return $(`-ios class chain:${introScr}`)
    }

    get invalid_eMailPasswordMessage()
    {
        return $('//*[@name="Whoops! Incorrect email or password. Try again."]');
    }

    get errorIcon_eMail()
    {
        return $('//android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.view.View'); //dont exists in iOS
    }

    get errorIcon_password()
    {
        return $('//android.widget.RelativeLayout[2]/android.view.View'); //dont exists in iOS
    }

    get resetPwd()
    {
        return $('//*[@name="FORGOT PASSWORD?  It happens."]')
        
    }
    
    // Login with valid creds - User data is from file
    async login()
    {
        var data = await Utils.readData();
        await this.loginPage_Email.setValue(data.e_mail);
        await this.loginPage_Password.setValue(data.password);
        await this.loginPage_LoginBtn.click();
    }


    // Login with invalid creds
    async login_invalidCreds(email,password)
    {
        await this.loginPage_Email.setValue(email);
        await this.loginPage_Password.setValue(password);
        await this.loginPage_LoginBtn.click();
        await this.invalid_eMailPasswordMessage.waitForDisplayed({timeout: 15000});
        // locator dont exists in iOS as textbox and icon are given the same name
        // await this.errorIcon_eMail.waitForDisplayed({timeout: 15000});
        // await this.errorIcon_password.waitForDisplayed({timeout: 15000});
    }
   }
module.exports = new LoginPage_iOS();
