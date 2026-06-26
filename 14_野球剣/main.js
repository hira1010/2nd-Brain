const { app, BrowserWindow } = require('electron');

let mainWindow = null;

app.on('ready', () => {
    // ウィンドウを作る
    mainWindow = new BrowserWindow({
        width: 1230,    // 幅
        height: 830,    // 高さも広く
    });
    
    // HTMLを読み込む
    mainWindow.loadFile('index.html');

   // ここでメニューバーを消す
    mainWindow.setMenu(null);
    
    // ウィンドウが閉じられたら
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
});