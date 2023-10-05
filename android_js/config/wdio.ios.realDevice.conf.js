const path = require('path')
const { config } = require('./wdio.shared.conf');

// ====================
// Runner Configuration
// ====================
config.port= 4723;

// ====================
// Specs
// ====================
config.specs= [
    // ToDo: define location for spec files here
    './android_js/test/specs/ios/test1.spec.js'
];

// ====================================
// Capabilities for all iOS scripts
// ====================================
config.capabilities = [
//     {
//         'appium:platformName': 'ios',
//         'appium:platformVersion': '16.4',
//         'appium:deviceName': 'iPhone 14 Pro',
//         'appium:automationName': 'XCUITest',
//         'appium:app': path.join(process.cwd(),'./android_js/app/ios/QA.ipa')
// }

//real device
{
    "appium:platformName": "iOS",
  "appium:platformVersion": "16.6.1",
  "appium:udid": "00008110-0002395E3CB9401E",
  "appium:automationName": "XCUITest",
  "appium:deviceName": "Kavitha's iPhone",
  "appium:app": "/Users/kavitha/Documents/QA/android_js/app/ios/QA.ipa",
  // /Users/kavitha/Documents/QA/android_js/app/ios/QA.ipa
  "appium:xcodeSigningId": "iPhone Developer",
  "appium:xcodeOrgId": "W7E68DX979"
}
];

exports.config = config;