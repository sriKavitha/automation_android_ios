const Utils = require('../../utils/helperUtils');
class MegaMillionsGamePage_iOS {

    get megaMillionsGame()
    {
        // return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains(\"mega\"))');
        return $('//XCUIElementTypeStaticText[@name="MEGABALL"]');
    }

    get mega_learnMore()
    {
        return $('(//XCUIElementTypeStaticText[@name="LEARN MORE >"])[1]');
    }

    get mega_winningNumbersTxt()
    {
        return $('~WINNING NUMBERS ');
    }

    get mega_nextDrawCurrentJackpotInfo()
    {
        return $('~Draws Tuesdays and Fridays');
    }
    
    get mega_winningNumbersInfo() //winning numbers container
    {
        const winningInfo = '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'
        return $(`-ios class chain:${winningInfo}`);
    }

    async mega_setNotifySwipe()
    {
        const getNotifications = await $('//XCUIElementTypeButton[@name="SET NOTIFICATIONS FOR THIS GAME"]')
        await driver.execute('mobile: scroll',{element: getNotifications.elementId, direction:"down"})
        console.log("asasasaasas\n\n\n\n")
        // return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains(\"SET NOTIFICATIONS FOR THIS GAME\"))');
    }

    get mega_setNotificationBtn()
    {
        return $('//XCUIElementTypeButton[@name="SET NOTIFICATIONS FOR THIS GAME"]');
    }

    get mega_setNotificationTitle()
    {
        return $('//*[@text="NOTIFICATIONS SETTINGS"]');
    }

    get mega_email()
    {
        const email = '**/XCUIElementTypeTextField[`value == "Email"`][1]'
        return $(`-ios class chain:${email}`)
    }

    get mega_password()
    {
        const pwd = '**/XCUIElementTypeSecureTextField[`value == "Password"`][1]'
        return $(`-ios class chain:${pwd}`)
        // return $('**/XCUIElementTypeSecureTextField[`value == "Password"`][1]')
    }

    get mega_loginBtn()
    {
        const loginBtn = '**/XCUIElementTypeButton[`label == "CREATE ACCOUNT"`]'
        return $(`-ios class chain:${loginBtn}`)
    }

    get goBtn()
    {
        return $('~Go');
    }

    async megaMillions_Login()
    {
        var data = await Utils.readData();
        await this.mega_email.setValue(data.e_mail);
        await this.mega_password.setValue(data.password);
        await this.goBtn.click();
        await (await this.mega_loginBtn).waitForDisplayed();
        await this.mega_loginBtn.click();
    }

    async megaMillionsGameScroll()
    {
        // const ele = await HomePage_iOS.intro //

        // await driver.execute('mobile: scroll', {element: ele.elementId, direction: 'right' }
        const mega = await this.megaMillionsGame;
        // console.log('MEGA DETAILS...',mega)
        // await driver.execute('mobile: scroll', {element: mega.elementId, direction: 'down'});
        // await driver.touchPerform({
        //     action: 'tap',
        //     options: {
        //       element: mega
        //     }
        //   });

        await driver.touchPerform([
            { action: 'press', options: { x: 320, y: 350 }},
            { action: 'wait', ms: 3000},
            { action: 'moveTo', options: { x: 80, y: 350 }},
            { action: 'release' }
          ])
          

        console.log("helllllooooooooo")
    }
   }
module.exports = new MegaMillionsGamePage_iOS();