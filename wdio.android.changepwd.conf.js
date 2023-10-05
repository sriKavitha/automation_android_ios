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
    './android_js/test/specs/android/MRMNYL=186_changePassword.spec.js'
];

// ================================================
// Capabilities for change password
// ================================================
config.capabilities = [
    {
        'appium:platformName': 'Android',
        'appium:platformVersion': '11.0',
        'appium:deviceName': 'Pixel 3',
        'appium:automationName': 'UIAutomator2',
        'appium:app': path.join(process.cwd(),'./android_js/app/android/app-qa.apk'),
        'appium:autoGrantPermissions':true,
        'appium:browserName': 'chrome',
        'appium:noReset':true
}
]
;

exports.config = config;