class FindRetailersPage {

    get findRetailersHeading()
    {
        return $('//XCUIElementTypeStaticText[@name="FIND RETAILERS"]')
    }

    // get findRetailersFilter()
    // {
    //     return $('//*[@resource-id="air.com.eprize.nylottery.app.NYLotteryApp:id/filtersButton"]');
    // } // dont have a locator in ios
    
    get findRetailersMap()
    {
        const retaiertsMap = "**/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther"
        return $(`-ios class chain:${retaiertsMap}`);
    }
}
module.exports = new FindRetailersPage();
