const Utils = require('../../utils/helperUtils');
// import { Key } from 'webdriverio'

class RegisterAccount {

    get eMail()
    {
        return $('//*[@value="Email"]');
    }

    get passWord()
    {
        return $('//*[@value="Password"]');
    }

    get confirmPassWord()
    {
        return $('//*[@value="Confirm Password"]');
    }

    get firstName()
    {
        const fName = '**/XCUIElementTypeTextField[`value == "First Name"`]'
        return $(`-ios class chain:${fName}`)
    }

    get lastName()
    {
        const lName = '**/XCUIElementTypeTextField[`value == "Last Name"`]';
        return $(`-ios class chain:${lName}`)
    }

    get phoneType()
    {
        return $('~Mobile');
    }

    get phNumber()
    {
        const ph = 'value == "(       )       -    "'
        return $(`-ios predicate string:${ph}`)
    }
    
    // Both Sure am! and Nope radio buttons are given same name... So clicking wont happen
    get major()
    {
        return $('//XCUIElementTypeApplication[@name="Official NY Lottery (qa)"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeButton[1]')
    }

    get zip()
    {
        return $('//*[@value="ZIP Code"]');
    }

    get createAccountBtn()
    {
        return $('//XCUIElementTypeButton[@name="CREATE ACCOUNT"]');
    }

    ////// Not sure if this works or not???
    get hourSymbol() 
    {
        return $('//*[@name="Creating Your Account"]')
    }

    get nextBtn()
    {
        return $('~Next:')
    }

    get doneBtn()
    {
        return $('//XCUIElementTypeStaticText[@name="Done"]')
    }
    

    // keyin values for the mandatory fields - email, pwd1, pwd2, last and first names, phone, zip
    async submitRegistrationForm()
    {
        var registrationDetails = [];

        var data = await Utils.readData();
        var dateTime = await Utils.currentTime();
       
        // generate the email in the format --> appEmailYYYY_HHMM@gmail.com
        var email = await "appEmail" + dateTime + "@gmail.com";
        
        await this.eMail.setValue(email);
        await this.passWord.setValue(data.password);
        await this.confirmPassWord.setValue(data.password);
        await this.firstName.setValue(data.firstName);
        await this.lastName.setValue(data.lastName);
        (await this.nextBtn).click()

        // tap on phone number to keyin the phone number
        await this.phNumber.setValue('2487779999');
        await this.major.click();
        
        // Keyin zipcode
        await this.zip.setValue(data.zipcode);
        (await this.doneBtn).click()

        await driver.pause(3000)
        console.log("I keyed in all the mandatory fields...")
        
        await this.createAccountBtn.click();
        
        // save the registration details
        await registrationDetails.push(data.firstName);
        await registrationDetails.push(data.lastName);
        await registrationDetails.push(email.toLowerCase());
        await registrationDetails.push("(248) 777 - 9999");
        await registrationDetails.push(data.zipcode);
        return registrationDetails;
    }
}
module.exports = new RegisterAccount();