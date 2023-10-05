class GuestPage_iOS {

    get getStartedBtn()
    {
        return $('//XCUIElementTypeStaticText[@name="GET STARTED"]');
    }  
    
    get allGamesTab()
    {
        return $('//XCUIElementTypeButton[@name="ALL GAMES"]');
    }
   }
module.exports = new GuestPage_iOS();