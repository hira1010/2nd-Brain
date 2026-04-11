/*:
 * @target MZ
 * @plugindesc 探索・謎解き支援プラグイン v1.1 - 接近検知・暗証番号・アイテム選択・合成
 * @author Antigravity
 *
 * @param SearchSwitch
 * @text 探索モード有効スイッチ
 * @desc このスイッチがONの時、アイテムへの接近検知が有効になります。
 * @type switch
 * @default 10
 *
 * @param HintIconIndex
 * @text ヒントアイコンのインデックス
 * @desc アイテムの近くで表示するアイコンID。
 * @type number
 * @default 192
 *
 * @param FoundItemsVariable
 * @text 発見済みアイテム数変数
 * @type variable
 * @default 12
 *
 * @param TotalItemsVariable
 * @text 目標アイテム数変数
 * @type variable
 * @default 13
 *
 * @param SelectedItemVariable
 * @text 選択中アイテムID格納変数
 * @desc アイテム選択画面で選ばれたアイテムのIDをここに格納します。
 * @type variable
 * @default 14
 *
 * @help SimpleSearchSystem.js (v1.1)
 *
 * 【主要機能】
 * 1. 接近検知: メモ欄に <search_item> と記述。
 * 2. 暗唱番号パネル: 4桁の入力画面。
 * 3. かっこいいアイテム選択: 探索中に手持ちのアイテムを選ぶ専用UI。
 * 4. アイテム合成: 二つのアイテムを組み合わせて新しいアイテムを作成。
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
 * @desc 所持品から使うアイテムを選んでもらいます。
 * @arg category
 * @text カテゴリ (1:通常, 2:貴重品)
 * @type select
 * @option 通常アイテム
 * @value 1
 * @option 貴重品
 * @value 2
 * @default 1
 *
 * @command combineItems
 * @text アイテム合成の実行
 * @desc 指定した二つのアイテムを消費し、新しいアイテムを一つ作成します。
 * @arg item1
 * @text 素材アイテム1
 * @type item
 * @arg item2
 * @text 素材アイテム2
 * @type item
 * @arg resultItem
 * @text 完成アイテム
 * @type item
 * @arg successCommonEvent
 * @text 合成成功時コモンイベント
 * @type common_event
 */

(() => {
    "use strict";

    const pluginName = "SimpleSearchSystem";
    const parameters = PluginManager.parameters(pluginName);
    const SW_SEARCH = Number(parameters["SearchSwitch"] || 10);
    const ICON_HINT = Number(parameters["HintIconIndex"] || 192);
    const VAR_FOUND = Number(parameters["FoundItemsVariable"] || 12);
    const VAR_TOTAL = Number(parameters["TotalItemsVariable"] || 13);
    const VAR_SELECTED_ITEM = Number(parameters["SelectedItemVariable"] || 14);

    //---------------------------------------------------------
    // プラグインコマンド
    //---------------------------------------------------------

    PluginManager.registerCommand(pluginName, "showDiscovery", args => {
        SceneManager._scene.showDiscoveryPopup(args.name, Number(args.iconIndex));
    });

    PluginManager.registerCommand(pluginName, "startNumPad", args => {
        SceneManager._scene.startNumPad(args.answer, Number(args.successCommonEvent), Number(args.failCommonEvent));
    });

    PluginManager.registerCommand(pluginName, "startItemSelection", args => {
        SceneManager._scene.startItemSelection(Number(args.category));
    });

    PluginManager.registerCommand(pluginName, "combineItems", args => {
        const i1 = Number(args.item1);
        const i2 = Number(args.item2);
        const res = Number(args.resultItem);
        const ce = Number(args.successCommonEvent);

        if ($gameParty.hasItem($dataItems[i1]) && $gameParty.hasItem($dataItems[i2])) {
            $gameParty.loseItem($dataItems[i1], 1);
            $gameParty.loseItem($dataItems[i2], 1);
            $gameParty.gainItem($dataItems[res], 1);
            SceneManager._scene.showDiscoveryPopup($dataItems[res].name, $dataItems[res].iconIndex);
            if (ce > 0) $gameTemp.reserveCommonEvent(ce);
        } else {
            SoundManager.playBuzzer();
        }
    });

    //---------------------------------------------------------
    // Window_SimpleItemSelect (アイテム選択窓)
    //---------------------------------------------------------

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
            if (this._category === 1) return DataManager.isItem(item) && item.itypeId === 1;
            if (this._category === 2) return DataManager.isItem(item) && item.itypeId === 2;
            return false;
        });
    };

    //---------------------------------------------------------
    // Scene_Map 拡張
    //---------------------------------------------------------

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this.createSearchUI();
    };

    Scene_Map.prototype.createSearchUI = function() {
        // 発見ポップアップ
        this._discoveryWindow = new Window_Discovery();
        this.addWindow(this._discoveryWindow);

        // アイテム選択窓
        const rect = new Rectangle(Graphics.width / 2 - 160, Graphics.height / 2 - 150, 320, 300);
        this._itemSelectWindow = new Window_SimpleItemSelect(rect);
        this._itemSelectWindow.setHandler("ok", () => {
            const item = this._itemSelectWindow.item();
            $gameVariables.setValue(VAR_SELECTED_ITEM, item ? item.id : 0);
            this._itemSelectWindow.close();
        });
        this._itemSelectWindow.setHandler("cancel", () => this._itemSelectWindow.close());
        this.addWindow(this._itemSelectWindow);

        // 探索HUD
        this._searchHUD = new Window_SearchHUD();
        this.addWindow(this._searchHUD);
    };

    Scene_Map.prototype.startItemSelection = function(category) {
        this._itemSelectWindow.setCategory(category);
        this._itemSelectWindow.show();
        this._itemSelectWindow.open();
        this._itemSelectWindow.activate();
        this._itemSelectWindow.select(0);
    };

    Scene_Map.prototype.startNumPad = function(answer, successCE, failCE) {
        this._numPadWindow = new Window_NumPad();
        this._numPadWindow.setHandler("ok", (result) => {
            if (result === answer) {
                if (successCE) $gameTemp.reserveCommonEvent(successCE);
            } else {
                if (failCE) $gameTemp.reserveCommonEvent(failCE);
            }
            this._numPadWindow.close();
            this._numPadWindow.deactivate();
        });
        this.addWindow(this._numPadWindow);
    };

    Scene_Map.prototype.showDiscoveryPopup = function(name, iconIndex) {
        this._discoveryWindow.setup(name, iconIndex);
    };

    //---------------------------------------------------------
    // 他のウィンドウクラス (前回の内容の統合)
    //---------------------------------------------------------

    function Window_Discovery() { this.initialize(...arguments); }
    Window_Discovery.prototype = Object.create(Window_Base.prototype);
    Window_Discovery.prototype.constructor = Window_Discovery;
    Window_Discovery.prototype.initialize = function() {
        const rect = new Rectangle(Graphics.width / 2 - 200, Graphics.height / 2 - 60, 400, 120);
        Window_Base.prototype.initialize.call(this, rect);
        this.openness = 0;
    };
    Window_Discovery.prototype.setup = function(name, iconIndex) {
        this.contents.clear();
        this.drawIcon(iconIndex, 10, 20);
        this.contents.fontSize = 24;
        this.drawText(name + " を発見！", 60, 20, 300, "center");
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

    function Window_NumPad() { this.initialize(...arguments); }
    Window_NumPad.prototype = Object.create(Window_Selectable.prototype);
    Window_NumPad.prototype.constructor = Window_NumPad;
    Window_NumPad.prototype.initialize = function() {
        const rect = new Rectangle(Graphics.width / 2 - 100, Graphics.height / 2 - 100, 200, 260);
        Window_Selectable.prototype.initialize.call(this, rect);
        this._digits = ["0", "0", "0", "0"];
        this.refresh();
        this.activate();
        this.select(0);
    };
    Window_NumPad.prototype.maxItems = function() { return 5; };
    Window_NumPad.prototype.drawItem = function(index) {
        const rect = this.itemRect(index);
        if (index < 4) this.drawText(this._digits[index], rect.x, rect.y, rect.width, "center");
        else this.drawText("UNLOCK", rect.x, rect.y, rect.width, "center");
    };
    Window_NumPad.prototype.processOk = function() {
        const idx = this.index();
        if (idx < 4) {
            this._digits[idx] = (parseInt(this._digits[idx]) + 1) % 10;
            this.refresh();
        } else {
            this.callOkHandler(this._digits.join(""));
        }
    };

    function Window_SearchHUD() { this.initialize(...arguments); }
    Window_SearchHUD.prototype = Object.create(Window_Base.prototype);
    Window_SearchHUD.prototype.constructor = Window_SearchHUD;
    Window_SearchHUD.prototype.initialize = function() {
        const rect = new Rectangle(Graphics.width - 220, 20, 200, 80);
        Window_Base.prototype.initialize.call(this, rect);
    };
    Window_SearchHUD.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if ($gameSwitches.value(SW_SEARCH)) {
            this.visible = true;
            this.refresh();
        } else {
            this.visible = false;
        }
    };
    Window_SearchHUD.prototype.refresh = function() {
        this.contents.clear();
        this.contents.fontSize = 18;
        this.changeTextColor(ColorManager.systemColor());
        this.drawText("アイテム探索中", 0, 0, 180, "center");
        this.changeTextColor(ColorManager.normalColor());
        const found = $gameVariables.value(VAR_FOUND);
        const total = $gameVariables.value(VAR_TOTAL);
        this.drawText(`${found} / ${total}`, 0, 25, 180, "center");
    };

    // 接近検知 (Sprite_Character) 
    const _Sprite_Character_update = Sprite_Character.prototype.update;
    Sprite_Character.prototype.update = function() {
        _Sprite_Character_update.call(this);
        this.updateSearchHint();
    };
    Sprite_Character.prototype.updateSearchHint = function() {
        if (!$gameSwitches.value(SW_SEARCH)) {
            if (this._searchHintSprite) this._searchHintSprite.visible = false;
            return;
        }
        const event = this._character;
        if (event instanceof Game_Event && event.event().meta.search_item) {
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
        }
    };

})();
