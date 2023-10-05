class AccountDetailsPage_iOS {
    get accountDetails_firstName()
    {
        return $('//*[@type="XCUIElementTypeTextField"][1]')
    }        
    
    get accountDetails_lastName()
    {
        return $('//*[@type="XCUIElementTypeTextField"][2]')
    }

    get accountDetails_eMail()
    {
        return $('//*[@type="XCUIElementTypeTextField"][3]')
    }
    
    get accountDetails_phone()
    {
        return $('//*[@type="XCUIElementTypeTextField"][4]')
    }

    get accountDetails_zip()
    {
        return $('//*[@type="XCUIElementTypeTextField"][5]')
    }

    get accountDetails_saveButton()
    {
        const saveBtn = '**/XCUIElementTypeButton[`label == "SAVE"`]';
        return $(`-ios class chain:${saveBtn}`);
    }

    // capture the registered user details from SETTINGS > Account Details screen
    async getAccountDeatils()
    {
        const acctDetails = [];
        
        await acctDetails.push(await this.accountDetails_firstName.getText());
        await acctDetails.push(await this.accountDetails_lastName.getText());
        await acctDetails.push(await this.accountDetails_eMail.getText());
        await acctDetails.push(await this.accountDetails_phone.getText());
        await acctDetails.push(await this.accountDetails_zip.getText());
        
        return acctDetails;
    }

}
module.exports = new AccountDetailsPage_iOS();
