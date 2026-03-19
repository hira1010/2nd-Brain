import { spawn } from 'child_process';
import * as fs from 'fs/promises';
import * as path from 'path';

const PROJECT_PATH = "C:/Users/hirak/Documents/RMMZ/Project1";
const DATA_PATH = path.join(PROJECT_PATH, "data");

async function editMap001() {
    console.log("Editing Map001 to add intro event...");
    const mapPath = path.join(DATA_PATH, "Map001.json");
    const content = await fs.readFile(mapPath, "utf-8");
    const map = JSON.parse(content);

    // 新しいイベントの作成 (ヒロインとの遭遇シーン)
    const newEvent = {
        "id": 3,
        "name": "導入シーン",
        "note": "",
        "pages": [
            {
                "conditions": {
                    "actorId": 1,
                    "actorValid": false,
                    "itemId": 1,
                    "itemValid": false,
                    "selfSwitchCh": "A",
                    "selfSwitchValid": false,
                    "switch1Id": 1,
                    "switch1Valid": false,
                    "switch2Id": 1,
                    "switch2Valid": false,
                    "variableId": 1,
                    "variableValid": false,
                    "variableValue": 0
                },
                "directionFix": false,
                "image": {
                    "tileId": 0,
                    "characterName": "SF_Actor3",
                    "direction": 2,
                    "pattern": 0,
                    "characterIndex": 3
                },
                "list": [
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["はぁ……はぁ……、だれ……？"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__148はふぅ", "pan": 0, "pitch": 100, "volume": 90 }] },
                    { "code": 231, "indent": 0, "parameters": [1, "heroine_01", 0, 0, 0, 0, 100, 100, 255, 0] }, // ピクチャ表示
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["見ないで……、こんな姿……っ！"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__192見ちゃだめ", "pan": 0, "pitch": 100, "volume": 90 }] },
                    { "code": 0, "indent": 0, "parameters": [] }
                ],
                "moveFrequency": 3,
                "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 1,
                "stepAnime": true,
                "through": false,
                "trigger": 0, // ボタンで開始
                "walkAnime": true
            }
        ],
        "x": 8,
        "y": 5
    };

    // イベント追加（既存の null 埋めを除去して追加）
    map.events[3] = newEvent;
    
    await fs.writeFile(mapPath, JSON.stringify(map, null, 0));
    console.log("Map001 updated with intro event.");
}

editMap001().catch(console.error);
