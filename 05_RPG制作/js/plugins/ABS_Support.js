/**
 * ABS_Support.js (Legacy Bridge)
 * 
 * v5.0 (Consolidated & Lightweight)
 * ・本プラグインの主要機能は ABS_Ultimate.js v15.2 以降に統合されました。
 * ・本ファイルは、既存のイベントや他プラグインとの互換性（ブリッジ）としてのみ機能します。
 */

(() => {
    'use strict';

    window.ABS = window.ABS || {};

    // ABS_Ultimate.js が読み込まれていない場合の最小限のガード
    if (!ABS.UI) {
        ABS.UI = {
            showInstructions: function() { console.warn('ABS_Ultimate.js is required for full functionality.'); }
        };
    }

    // 互換性ブリッジ (Legacy Bridge)
    // 既存のイベントコマンド等から直接呼ばれていた関数を新しいパスへ転送します。
    
    ABS.showInstructions = function() {
        if (ABS.UI && ABS.UI.showInstructions) ABS.UI.showInstructions();
    };

    ABS.showOnomaList = function() {
        if (ABS.UI && ABS.UI.showWeaponList) ABS.UI.showWeaponList();
    };

    ABS.throwOnoma = function() {
        if (ABS.Combat && ABS.Combat.fireProjectile) ABS.Combat.fireProjectile();
    };

    console.log('ABS_Support.js: v5.0 (Legacy Bridge) Loaded.');

})();
