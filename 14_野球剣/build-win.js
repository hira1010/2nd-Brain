const builder = require('electron-builder');

builder.build({
    config: {
        appId: 'com.nurebaya.holywater',
        productName: 'いもうとのももはとじゃんけんすることになった',
        directories: {
            output: 'dist'
        },
        win: {
            target: {
                target: 'nsis',
                arch: ['x64']
            },
          //  icon: 'favicon.ico'
        },
        nsis: {
            oneClick: false,
            allowToChangeInstallationDirectory: true
        }
    }
});