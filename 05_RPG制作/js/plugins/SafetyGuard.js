/*:
 * @target MZ
 * @plugindesc SafetyGuard v1.0 (アンチ・クラッシュ)
 * @author Antigravity
 * 
 * @help 
 * 画像や音声ファイルが足りなくても、Retry画面でゲームが止まらないようにします。
 */

(() => {
    "use strict";

    // 1. AudioManager 強化
    const _AM_createBuffer = AudioManager.createBuffer;
    AudioManager.createBuffer = function(folder, name) {
        try {
            const buffer = _AM_createBuffer.call(this, folder, name);
            if (buffer) {
                buffer.addLoadListener(() => {
                    if (buffer.isError()) {
                        console.warn("AUDIO MISSING (Safe):", folder + "/" + name);
                        buffer._error = null;
                    }
                });
            }
            return buffer;
        } catch (e) {
            return { addLoadListener: () => {}, isError: () => false };
        }
    };

    // 2. ImageManager 強化
    const _IM_loadBitmap = ImageManager.loadBitmap;
    ImageManager.loadBitmap = function(folder, name) {
        try {
            const bitmap = _IM_loadBitmap.call(this, folder, name);
            if (bitmap) {
                bitmap.addLoadListener(() => {
                    if (bitmap.isError()) {
                        console.warn("IMAGE MISSING (Safe):", folder + name);
                        bitmap._error = null;
                    }
                });
            }
            return bitmap;
        } catch (e) {
            return ImageManager.loadEmptyBitmap();
        }
    };
})();
