// const path = require('path')
const { config } = require('./wdio.shared.conf');

// ====================
// Runner Configuration
// ====================
// config.port= 4723;
config.user = "kavithasriram_9ytrEp";
config.key = "mysn58zDhs6XvvGkyydh"

// ====================
// Specs
// ====================
config.specs= [
    // ToDo: define location for spec files here
    './android_js/test/specs/android/MRMNYL-191.spec.js'
];

// ====================================
// Capabilities for all Android scripts
// ====================================
config.capabilities = [
//     {
//         'platformName': 'Android',
//         'appium:platformVersion': '9.0',
//         'appium:deviceName': 'Google Pixel 3',
//         'appium:automationName': 'UIAutomator2',
//         'appium:app': 'bs://2d4b18055b902d15ea00c7b4fc065e64241622fb', 
//         'appium:autoGrantPermissions':true
// }
{
    "appium:platformName": "iOS",
  "appium:platformVersion": "16.6",
//   "appium:udid": "00008110-0002395E3CB9401E",
  "appium:automationName": "XCUITest",
  "appium:deviceName": "iPhone 14",
  "appium:app": "bs://57fa876ec68f3edbbde9ea54bcba9c5a089a79bc",
//   "appium:xcodeSigningId": "iPhone Developer",
//   "appium:xcodeOrgId": "W7E68DX979"
}
]
config.services=['browserstack']
;

exports.config = config;