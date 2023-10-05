class PromotionsPage_iOS {

    get promotionsHeading()
    {
        return $('//XCUIElementTypeStaticText[@name="PROMOTIONS"]')
    }

    ///////// the screen in lower env is broken cant locate the elements
    //////// the content in cms has been changed with warning image than "we are open"
    // get promotionsTitle()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/txt_promotion_title"]');
    // }
    
    // get promotionsIcon()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/img_promtion"]');
    // }
    get promotionsBtn()
    {
        const promotionsButton = '**/XCUIElementTypeNavigationBar[`name == "GAMES"`]/XCUIElementTypeButton[2]'
        return $(`-ios class chain:${promotionsButton}`)

    }

}
module.exports = new PromotionsPage_iOS();
