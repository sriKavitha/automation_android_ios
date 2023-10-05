const Utils = require('../../utils/helperUtils');

class LottoPage {
   
    get gameNumberOfBalls()
    {
        const balls= '**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]'
        return $$(`-ios class chain:${balls}`)
    }

    get lotto_WinningNumbers()
    {
        return $('~WINNING NUMBERS ');
    }

    get lotto_Drawings()
    {
        return $('~NEXT DRAWING ');
    }

    get NumberGame()
    {
        return $('android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("WINNING"))');
    }

    async swipeLottoGame()
    {
        const thisgame_balls = 7
        await Utils.swipeTillGame(this,thisgame_balls);
    }

}
module.exports = new LottoPage();
