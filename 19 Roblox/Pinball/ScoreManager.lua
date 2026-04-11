-- ScoreManager.lua: スコア管理モジュール
-- ReplicatedStorage に IntValue "Score" を作成し、StarterGui に UI を表示します。

local ScoreManager = {}

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

-- スコア用 IntValue を取得または作成
local function getScoreValue()
    local score = ReplicatedStorage:FindFirstChild("Score")
    if not score then
        score = Instance.new("IntValue")
        score.Name = "Score"
        score.Value = 0
        score.Parent = ReplicatedStorage
    end
    return score
end

local function createUI()
    local player = Players.LocalPlayer
    if not player then return end
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "PinballScoreGui"
    screenGui.ResetOnSpawn = false
    screenGui.Parent = player:WaitForChild("PlayerGui")

    local label = Instance.new("TextLabel")
    label.Name = "ScoreLabel"
    label.Size = UDim2.new(0, 200, 0, 50)
    label.Position = UDim2.new(0, 10, 0, 10)
    label.BackgroundTransparency = 0.5
    label.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
    label.TextColor3 = Color3.fromRGB(255, 255, 255)
    label.TextScaled = true
    label.Font = Enum.Font.SourceSansBold
    label.Text = "Score: 0"
    label.Parent = screenGui

    -- スコアが変わったら UI を更新
    local scoreValue = getScoreValue()
    scoreValue.Changed:Connect(function(newVal)
        label.Text = "Score: " .. tostring(newVal)
    end)
end

function ScoreManager.addScore(amount)
    local score = getScoreValue()
    score.Value = score.Value + amount
end

function ScoreManager.init()
    -- UI を作成（ローカルスクリプト側で呼び出す）
    createUI()
end

return ScoreManager
