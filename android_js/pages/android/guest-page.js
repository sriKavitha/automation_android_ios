class GuestPage {

    get getStartedBtn()
    {
        return $('//*[@text = "GET STARTED"]');
    }  
    
    get allGamesTab()
    {
        return $('//*[@text = "ALL GAMES"]');
    }

    // get QuickDrawGame()
    // {
    //     // return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("QUICK DRAW")');
    //     return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains(\"QUICK DRAW\"))')
    //     // await driver.pause(2000);
    //     // await $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("LEARN MORE >")');
    // }

    // get quickDraw_WinningNumbers_DrawNumbers()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/winningNumbersContainer"]');       
    // }

    // get quickDraw_GetLuckyNumbersToPlay()
    // {
    //     return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("GET LUCKY NUMBERS TO PLAY")');
    //     // return $('//*[@text="GET LUCKY NUMBERS TO PLAY"]')
    // }

    // get quickDraw_viewDraws()
    // {
    //     return $('//*[@text= "VIEW DRAWS"]')
    // }

    // get quickDraw_DrawNumber()
    // {
    //     return $('//*[@text,"DRAW NUMBER")]');       
    // }
    // 
    // get createAccountHome()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/loginRegister"]')
    // }

    // get loginBtnHomePage()
    // {
    //     return $('//*[@resource-id = "air.com.eprize.nylottery.app.NYLotteryApp:id/loginButton"]');
    // }

    // get countinueGuestBtnHomePage()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/guestButton"]')
    // }
   }
module.exports = new GuestPage();