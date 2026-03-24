import * as fs from 'fs/promises';
import * as path from 'path';

const PROJECT_PATH = "C:/Users/hirak/Documents/RMMZ/Project1";
const DATA_PATH = path.join(PROJECT_PATH, "data");

async function addCaveEvent() {
    console.log("Adding cave animation event to Map001...");
    const mapPath = path.join(DATA_PATH, "Map001.json");
    const content = await fs.readFile(mapPath, "utf-8");
    const map = JSON.parse(content);

    // 洞窟入口のイベント (座標はスクリーンショットから推測: 10, 1)
    const caveEvent = {
        "id": 4,
        "name": "洞窟の乳首演出",
        "note": "",
        "pages": [
            {
                "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
                "directionFix": false,
                "image": { "tileId": 0, "characterName": "", "direction": 2, "pattern": 0, "characterIndex": 0 },
                "list": [
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__93いっぱい出してぇ！！", "pan": 0, "pitch": 100, "volume": 100 }] },
                    { "code": 231, "indent": 0, "parameters": [2, "heroine_02", 0, 0, 0, 0, 100, 100, 255, 0] }, // 新しい画像表示
                    { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 5, 10, true] }, // フラッシュ（噴射演出）
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "ヒロイン"] },
                    { "code": 401, "indent": 0, "parameters": ["んぁっ！ 洞窟の冷気で……乳首から溢れちゃうぅぅ！！"] },
                    { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 3, 20, true] }, // 追いフラッシュ
                    { "code": 235, "indent": 0, "parameters": [2] }, // ピクチャ消去
                    { "code": 201, "indent": 0, "parameters": [0, 2, 8, 8, 0, 0] }, // 本来の洞窟移動 (Map 2へ)
                    { "code": 0, "indent": 0, "parameters": [] }
                ],
                "moveFrequency": 3,
                "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 0,
                "stepAnime": false,
                "through": false,
                "trigger": 1, // プレイヤー接触
                "walkAnime": true
            }
        ],
        "x": 10,
        "y": 1
    };

    map.events[4] = caveEvent;
    await fs.writeFile(mapPath, JSON.stringify(map, null, 0));
    console.log("Cave event added successfully.");
}

addCaveEvent().catch(console.error);
