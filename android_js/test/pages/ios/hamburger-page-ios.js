const Utils = require('../../utils/helperUtils');

class HamburgerPage_iOS {

    // ios does not have hamburger icon. But, all the buttons are given the same name, when this button is clicked, it clicks RETAILERS button
    get hamburgerIcon()
    {
        const btn = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton'
        return $(`-ios class chain:${btn}`);
    }

    // This element is not locatable as all the buttons at the bottom has same name... dont know if it works or not
    get settingsBtn() 
    {
        const btn = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton'
        return $(`-ios class chain:${btn}`);
    }

    get settingsTxt()
    {
        return $('//XCUIElementTypeStaticText[@name="SETTINGS"]');
    }

    // get homeScreen_megaMillions()
    // {
    //     return $('//XCUIElementTypeStaticText[@name="MEGA MILLIONS"]')
    // }

    get settings_Email()
    {
        const emailTxtbox = '**/XCUIElementTypeTextField[`value == "Email"`]'
        return $(`-ios class chain:${emailTxtbox}`)
    }

    get settings_Password()
    {
        const passwordTxtbox = '**/XCUIElementTypeTextField[`value == "Password"`]'
        return $(`ios class chain:${passwordTxtbox}`)
    }

    get settings_LogInBtn()
    {
        return $('//XCUIElementTypeStaticText[@name="LOGIN"]');
    }

    get settings_Loginbtn()
    {
        return $('(//XCUIElementTypeStaticText[@name="LOG IN"])[2]');
    } 

    get promotionsBtn()
    {
        return $('~PROMOTIONS');
    }

    // cant access this element for iOS
    // get findRetailersBtn()
    // {
    //     return $('//*[@text="FIND RETAILERS"]');
    // }
    
    async settings_Login()
    {
        var data = await Utils.readData();
        await this.settings_Email.setValue(data.e_mail);
        await this.settings_Password.setValue(data.password);
        await this.settings_Loginbtn.click();
    }
    
   }
module.exports = new HamburgerPage_iOS();