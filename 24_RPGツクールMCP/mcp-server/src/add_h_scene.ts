import * as fs from 'fs/promises';
import * as path from 'path';

const PROJECT_PATH = "C:/Users/hirak/Documents/RMMZ/Project1";
const DATA_PATH = path.join(PROJECT_PATH, "data");

async function createHScene() {
    console.log("Creating full H-scene on Map001...");
    const mapPath = path.join(DATA_PATH, "Map001.json");
    const content = await fs.readFile(mapPath, "utf-8");
    const map = JSON.parse(content);

    const hEvent = {
        "id": 3,
        "name": "Hイベント",
        "note": "",
        "pages": [
            {
                "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
                "directionFix": false,
                "image": { "tileId": 0, "characterName": "SF_Actor3", "direction": 2, "pattern": 1, "characterIndex": 3 },
                "list": [
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["あ、あなた……そんなに興奮した目で見て……っ。"] },
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["や、やめて……見ないで……！"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__192見ちゃだめ", "pan": 0, "pitch": 100, "volume": 100 }] },
                    { "code": 223, "indent": 0, "parameters": [[-68, -68, -68, 0], 60, true] }, // 画面の色調変更（暗く）
                    { "code": 231, "indent": 0, "parameters": [1, "heroine_01", 0, 0, 0, 0, 100, 100, 255, 0] }, // 画像表示
                    { "code": 223, "indent": 0, "parameters": [[0, 0, 0, 0], 60, true] }, // 戻す
                    
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["んぁっ……、そんな……奥まで……っ！？"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__116おくきたぁ", "pan": 0, "pitch": 100, "volume": 100 }] },
                    { "code": 221, "indent": 0, "parameters": [5, 5, 20, true] }, // 画面のシェイク
                    
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["もうダメ……、い、イッちゃうぅぅ！！"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__172もうだめぇぇぇぇ！！", "pan": 0, "pitch": 100, "volume": 100 }] },
                    { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 3, 20, true] }, // フラッシュ（絶頂）

                    { "code": 235, "indent": 0, "parameters": [1, 255, 60, false] }, // ピクチャの消去
                    { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
                    { "code": 401, "indent": 0, "parameters": ["はぁ……はぁ……。ひどいこと……するのね……。"] },
                    { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__148はふぅ", "pan": 0, "pitch": 100, "volume": 100 }] },
                    
                    { "code": 122, "indent": 0, "parameters": [3, 3, 1, 0, 1] }, // 絶頂回数変数 +1
                    { "code": 0, "indent": 0, "parameters": [] }
                ],
                "moveFrequency": 3,
                "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 1,
                "stepAnime": true,
                "through": false,
                "trigger": 0,
                "walkAnime": true
            }
        ],
        "x": 8, // スクリーンショットのプレイヤー位置に近い場所に調整
        "y": 6
    };

    map.events[3] = hEvent;
    await fs.writeFile(mapPath, JSON.stringify(map, null, 0));
    console.log("H-scene added successfully.");
}

createHScene().catch(console.error);
