const path = require("path");
const fs = require("node:fs/promises");
const GuestPage = require('../pages/android/guest-page');
class Utils {

  // read jsonfile
  async readData() {
    const data = await fs.readFile("./android_js/test/data/appUserDetails.json");
    var userData = [];
    try {
       userData = JSON.parse(data);
    } catch (error) {
      console.log("File not found", error);
    }
    return userData;
  }

  // Generate current time - YYYY_HHMM
  async currentTime() {
    const yr = new Date().getFullYear();
    const min = new Date().getMinutes();
    const hr = new Date().getHours();
    const ss = new Date().getSeconds();
    const currenttime = yr + "_" + hr + min + ss;
    return currenttime; 
  }

  // swipe intro cards and tap GET STARTED button
  async swipe()
  {
      for(var i=1;i<=5;i++)
      {
         await $('android=new UiScrollable(new UiSelector().scrollable(true)).setAsHorizontalList().scrollForward()');
         await driver.pause(1000);
      }
      // await driver.pause(3000);
      await GuestPage.getStartedBtn.waitForDisplayed();
      await GuestPage.getStartedBtn.click();
  }
}
module.exports = new Utils();
