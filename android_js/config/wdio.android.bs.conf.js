const {config} = require('../config/wdio.shared.conf')

// ====================
// Runner Configuration
// ====================
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
config.capabilities = [{
        'platformName': 'Android',
        'appium:platformVersion': '9.0',
        'appium:deviceName': 'Google Pixel 3',
        'appium:automationName': 'UIAutomator2',
        'appium:app': 'bs://2d4b18055b902d15ea00c7b4fc065e64241622fb',
        'appium:autoGrantPermissions':true
}]
config.services=['browserstack']
;

exports.config = config;