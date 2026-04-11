-- Init.lua: ピンボールゲームの初期化スクリプト
-- StarterPlayerScripts に配置し、ゲーム開始時に全モジュールをロードします。

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

-- モジュールの取得
local Table = require(script.Parent.Table)
local Ball = require(script.Parent.Ball)
local Flipper = require(script.Parent.FlipperControl)
local ScoreManager = require(script.Parent.ScoreManager)

-- 1. テーブルと壁・バンパーを生成
local workspaceFolder = Instance.new("Folder")
workspaceFolder.Name = "PinballWorkspace"
workspaceFolder.Parent = workspace

Table.create(workspaceFolder)

-- 2. ボールを生成
Ball.spawn(workspaceFolder)

-- 3. フリッパーを配置
Flipper.setup(workspaceFolder)

-- 4. スコア UI を初期化（ローカル側で実行）
ScoreManager.init()

-- 5. MCP 接続テスト（Roblox Studio 側の MCP が有効か確認）
local function testMCP()
    local success, result = pcall(function()
        -- AI に対して簡単な問い合わせを送信
        return game:GetService("Chat"):Chat(Players.LocalPlayer.Character, "Roblox Studio とつながっていますか？", Enum.ChatColor.Blue)
    end)
    if not success then
        warn("MCP 接続テストに失敗しました: " .. tostring(result))
    else
        print("MCP 接続テストを送信しました（結果は AI 側で確認してください）")
    end
end

-- ゲーム開始時に MCP テストを実行
if RunService:IsRunning() then
    testMCP()
end

return {}
