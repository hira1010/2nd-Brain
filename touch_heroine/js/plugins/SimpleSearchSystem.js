/*:
 * @target MZ
 * @plugindesc [SEA] 探索・謎解き支援プラグイン v2.0 - リファクタリング版
 * @author Antigravity
 *
 * @param VariableSettings
 * @text 【変数設定】
 *
 * @param FoundItemsVariable
 * @parent VariableSettings
 * @text [SEA] 発見アイテム数 (Variable ID)
 * @type variable
 * @default 12
 *
 * @param TotalItemsVariable
 * @parent VariableSettings
 * @text [SEA] 目標アイテム数 (Variable ID)
 * @type variable
 * @default 13
 *
 * @param SelectedItemVariable
 * @parent VariableSettings
 * @text [SEA] 選択中アイテムID (Variable ID)
 * @type variable
 * @default 14
 *
 * @param SwitchSettings
 * @text 【スイッチ設定】
 *
 * @param SearchSwitch
 * @parent SwitchSettings
 * @text [SEA] 探索モード (Switch ID)
 * @type switch
 * @default 11
 *
 * @param IconSettings
 * @text 【アイコン設定】
 *
 * @param HintIconIndex
 * @parent IconSettings
 * @text ヒントアイコンのインデックス
 * @desc アイテムの近くで表示するアイコンID。
 * @type number
 * @default 192
 *
 * @help SimpleSearchSystem.js (v2.0)
 *
 * 探索パートの謎解きやアイテム発見をサポートするプラグインです。
 * v2.0へのリファクタリングでコードを整理しました。
 *
 * @command showDiscovery
 * @text 発見ポップアップ表示
 * @arg name
 * @text アイテム名
 * @arg iconIndex
 * @text アイコンID
 *
 * @command startNumPad
 * @text 暗証番号入力の開始
 * @arg answer
 * @text 正解の番号
 * @default 1234
 * @arg successCommonEvent
 * @text 正解時コモンイベント
 * @type common_event
 * @arg failCommonEvent
 * @text 不正解時コモンイベント
 * @type common_event
 *
 * @command startItemSelection
 * @text アイテム選択画面の表示
 * @arg category
 * @text カテゴリ (1:通常, 2:貴重品)
 * @type select
 * @option 通常アイテム
 * @value 1
 * @option 貴重品
 * @value 2
 * @default 1
 */

(() => {
    "use strict";

    const pluginName = "SimpleSearchSystem";
    const params = PluginManager.parameters(pluginName);

    const VAR_FOUND = Number(params["FoundItemsVariable"] || 12);
    const VAR_TOTAL = Number(params["TotalItemsVariable"] || 13);
    const VAR_SELECTED_ITEM = Number(params["SelectedItemVariable"] || 14);
    const SW_SEARCH = Number(params["SearchSwitch"] || 11);
    const ICON_HINT = Number(params["HintIconIndex"] || 192);

    //-----------------------------------------------------------------------------
    // プラグインコマンドの登録
    //-----------------------------------------------------------------------------

    PluginManager.registerCommand(pluginName, "showDiscovery", args => {
        if (SceneManager._scene instanceof Scene_Map) {
            SceneManager._scene.showDiscoveryPopup(args.name, Number(args.iconIndex));
        }
    });

    PluginManager.registerCommand(pluginName, "startNumPad", args => {
        if (SceneManager._scene instanceof Scene_Map) {
            SceneManager._scene.startNumPad(args.answer, Number(args.successCommonEvent), Number(args.failCommonEvent));
        }
    });

    PluginManager.registerCommand(pluginName, "startItemSelection", args => {
        if (SceneManager._scene instanceof Scene_Map) {
            SceneManager._scene.startItemSelection(Number(args.category));
        }
    });

    //-----------------------------------------------------------------------------
    // Window_SimpleItemSelect
    // 探索中にアイテムを選択するためのシンプルなリスト窓
    //-----------------------------------------------------------------------------

    function Window_SimpleItemSelect() {
        this.initialize(...arguments);
    }
    Window_SimpleItemSelect.prototype = Object.create(Window_ItemList.prototype);
    Window_SimpleItemSelect.prototype.constructor = Window_SimpleItemSelect;

    Window_SimpleItemSelect.prototype.initialize = function(rect) {
        Window_ItemList.prototype.initialize.call(this, rect);
        this.hide();
        this.deactivate();
    };

    Window_SimpleItemSelect.prototype.maxCols = function() { return 1; };
    Window_SimpleItemSelect.prototype.needsNumber = function() { return false; };

    Window_SimpleItemSelect.prototype.makeItemList = function() {
        this._data = $gameParty.allItems().filter(item => {
            if (!item) return false;
            return DataManager.isItem(item) && item.itypeId === this._category;
        });
    };

    //-----------------------------------------------------------------------------
    // Window_Discovery
    // アイテム発見時に表示されるポップアップ
    //-----------------------------------------------------------------------------

    function Window_Discovery() { this.initialize(...arguments); }
    Window_Discovery.prototype = Object.create(Window_Base.prototype);
    Window_Discovery.prototype.constructor = Window_Discovery;

    Window_Discovery.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.openness = 0;
        this._duration = 0;
    };

    Window_Discovery.prototype.setup = function(name, iconIndex) {
        this.contents.clear();
        this.drawIcon(iconIndex, 10, this.innerHeight / 2 - 16);
        this.contents.fontSize = 24;
        this.drawText(name + " を発見！", 60, 0, this.innerWidth - 70, "left");
        this.open();
        this._duration = 180;
        SoundManager.playRecovery();
    };

    Window_Discovery.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (this._duration > 0) {
            this._duration--;
            if (this._duration === 0) this.close();
        }
    };

    //-----------------------------------------------------------------------------
    // Window_NumPad
    // 4桁の数値入力を管理するウィンドウ
    //-----------------------------------------------------------------------------

    function Window_NumPad() { this.initialize(...arguments); }
    Window_NumPad.prototype = Object.create(Window_Selectable.prototype);
    Window_NumPad.prototype.constructor = Window_NumPad;

    Window_NumPad.prototype.initialize = function(rect) {
        Window_Selectable.prototype.initialize.call(this, rect);
        this._digits = ["0", "0", "0", "0"];
        this.refresh();
        this.activate();
        this.select(0);
    };

    Window_NumPad.prototype.maxItems = function() { return 5; };

    Window_NumPad.prototype.drawItem = function(index) {
        const rect = this.itemRect(index);
        if (index < 4) {
            this.drawText(this._digits[index], rect.x, rect.y, rect.width, "center");
        } else {
            this.changeTextColor(ColorManager.systemColor());
            this.drawText("UNLOCK", rect.x, rect.y, rect.width, "center");
            this.resetTextColor();
        }
    };

    Window_NumPad.prototype.processOk = function() {
        const idx = this.index();
        if (idx < 4) {
            this._digits[idx] = (parseInt(this._digits[idx]) + 1) % 10;
            SoundManager.playCursor();
            this.refresh();
        } else {
            this.callOkHandler(this._digits.join(""));
        }
    };

    //-----------------------------------------------------------------------------
    // Window_SearchHUD
    // 画面右上に現在の探索状況を表示する
    //-----------------------------------------------------------------------------

    function Window_SearchHUD() { this.initialize(...arguments); }
    Window_SearchHUD.prototype = Object.create(Window_Base.prototype);
    Window_SearchHUD.prototype.constructor = Window_SearchHUD;

    Window_SearchHUD.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
    };

    Window_SearchHUD.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        this.visible = $gameSwitches.value(SW_SEARCH);
        if (this.visible) this.refresh();
    };

    Window_SearchHUD.prototype.refresh = function() {
        this.contents.clear();
        this.contents.fontSize = 18;
        this.changeTextColor(ColorManager.systemColor());
        this.drawText("アイテム探索中", 0, 0, this.innerWidth, "center");
        this.changeTextColor(ColorManager.normalColor());
        const found = $gameVariables.value(VAR_FOUND);
        const total = $gameVariables.value(VAR_TOTAL);
        this.drawText(`${found} / ${total}`, 0, 25, this.innerWidth, "center");
    };

    //-----------------------------------------------------------------------------
    // Scene_Map 拡張
    //-----------------------------------------------------------------------------

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this.createSearchSystemWindows();
    };

    Scene_Map.prototype.createSearchSystemWindows = function() {
        // ポップアップ
        this._discoveryWindow = new Window_Discovery(new Rectangle(Graphics.width / 2 - 200, 100, 400, 100));
        this.addWindow(this._discoveryWindow);

        // アイテム選択
        const rect = new Rectangle(Graphics.width / 2 - 160, Graphics.height / 2 - 150, 320, 300);
        this._itemSelectWindow = new Window_SimpleItemSelect(rect);
        this._itemSelectWindow.setHandler("ok", () => {
            const item = this._itemSelectWindow.item();
            $gameVariables.setValue(VAR_SELECTED_ITEM, item ? item.id : 0);
            this._itemSelectWindow.close();
            this._itemSelectWindow.deactivate();
        });
        this._itemSelectWindow.setHandler("cancel", () => {
            this._itemSelectWindow.close();
            this._itemSelectWindow.deactivate();
        });
        this.addWindow(this._itemSelectWindow);

        // HUD
        this._searchHUD = new Window_SearchHUD(new Rectangle(Graphics.width - 220, 20, 200, 100));
        this.addWindow(this._searchHUD);
    };

    Scene_Map.prototype.startItemSelection = function(category) {
        this._itemSelectWindow.setCategory(category);
        this._itemSelectWindow.refresh();
        this._itemSelectWindow.show();
        this._itemSelectWindow.open();
        this._itemSelectWindow.activate();
        this._itemSelectWindow.select(0);
    };

    Scene_Map.prototype.startNumPad = function(answer, successCE, failCE) {
        const rect = new Rectangle(Graphics.width / 2 - 100, Graphics.height / 2 - 130, 200, 260);
        this._numPadWindow = new Window_NumPad(rect);
        this._numPadWindow.setHandler("ok", (result) => {
            const isCorrect = (result === answer);
            SoundManager.playOk();
            if (isCorrect && successCE) $gameTemp.reserveCommonEvent(successCE);
            if (!isCorrect && failCE) $gameTemp.reserveCommonEvent(failCE);
            this._numPadWindow.close();
            this._numPadWindow.deactivate();
        });
        this._numPadWindow.setHandler("cancel", () => {
            this._numPadWindow.close();
        });
        this.addWindow(this._numPadWindow);
    };

    Scene_Map.prototype.showDiscoveryPopup = function(name, iconIndex) {
        this._discoveryWindow.setup(name, iconIndex);
    };

    //-----------------------------------------------------------------------------
    // Sprite_Character 拡張 (接近ヒント表示)
    //-----------------------------------------------------------------------------

    const _Sprite_Character_update = Sprite_Character.prototype.update;
    Sprite_Character.prototype.update = function() {
        _Sprite_Character_update.call(this);
        this.updateSearchHint();
    };

    Sprite_Character.prototype.updateSearchHint = function() {
        const event = this._character;
        if (!event || !(event instanceof Game_Event)) return;
        
        if (!$gameSwitches.value(SW_SEARCH) || !event.event().meta.search_item) {
            if (this._searchHintSprite) this._searchHintSprite.visible = false;
            return;
        }

        const player = $gamePlayer;
        const dist = Math.abs(event.x - player.x) + Math.abs(event.y - player.y);
        
        if (dist <= 2) {
            if (!this._searchHintSprite) {
                this._searchHintSprite = new Sprite();
                this._searchHintSprite.bitmap = ImageManager.loadSystem("IconSet");
                this._searchHintSprite.setFrame((ICON_HINT % 16) * 32, Math.floor(ICON_HINT / 16) * 32, 32, 32);
                this._searchHintSprite.anchor.x = 0.5;
                this._searchHintSprite.anchor.y = 1;
                this.addChild(this._searchHintSprite);
            }
            this._searchHintSprite.y = -48 + Math.sin(Graphics.frameCount / 10) * 5;
            this._searchHintSprite.visible = true;
        } else if (this._searchHintSprite) {
            this._searchHintSprite.visible = false;
        }
    };

})();
