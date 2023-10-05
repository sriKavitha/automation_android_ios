const path = require('path')
const { config } = require('../QA/wdio.shared.conf');

// ====================
// Runner Configuration
// ====================
config.port= 4723;
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
        'appium:platformVersion': '12.0',
        'appium:deviceName': 'RF8M317MXDK',
        'appium:automationName': 'UIAutomator2',
        'appium:app': path.join(process.cwd(),'./android_js/app/android/app-qa.apk'),
        'appium:autoGrantPermissions':true
}]
;

exports.config = config;