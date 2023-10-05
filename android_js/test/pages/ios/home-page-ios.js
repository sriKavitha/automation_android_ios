
class HomePage_iOS {

    get threeButtons()
    {
        // return $('//XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther'); ///// not a valid one... just in case
        // return $('~NYL_MobileApp_01LogIn_bg.png');
        return $('//XCUIElementTypeImage[@name="NYL_MobileApp_01LogIn_bg.png"]');
    }                               

    get createAccountHome()
    {
        return $('//XCUIElementTypeButton[@name="CREATE ACCOUNT"]');
    }

    get loginBtnHomePage()
    {
        return $('//XCUIElementTypeButton[@name="LOG IN"]');
    }

    get countinueGuestBtnHomePage()
    {
        return $('//XCUIElementTypeStaticText[@name="CONTINUE AS GUEST"]');
    }
    get intro()
    {
        const introScr = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
        return $(`-ios class chain:${introScr}`)
    }
   }
module.exports = new HomePage_iOS();
