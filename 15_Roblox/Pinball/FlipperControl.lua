-- FlipperControl.lua: キーボード入力で左右フリッパーを回転させるローカルスクリプト
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")

local FLIPPER_ANGLE = math.rad(45) -- 45度回転
local FLIPPER_SPEED = 0.2 -- 回転にかかる時間（秒）

local function createFlipper(name, hingeCFrame, parent)
    local flipper = Instance.new("Part")
    flipper.Name = name
    flipper.Size = Vector3.new(2, 0.5, 6)
    flipper.Anchored = true
    flipper.CanCollide = true
    flipper.Color = Color3.fromRGB(200, 200, 200)
    flipper.CFrame = hingeCFrame
    flipper.Parent = parent
    return flipper
end

local Flipper = {}
Flipper.left = nil
Flipper.right = nil
Flipper.leftTarget = 0
Flipper.rightTarget = 0

function Flipper.setup(parent)
    local tablePos = parent.Position
    local y = tablePos.Y + 5
    -- 左フリッパーのヒンジ位置
    local leftPos = Vector3.new(tablePos.X - 20, y, tablePos.Z + 80)
    Flipper.left = createFlipper("LeftFlipper", CFrame.new(leftPos), parent)
    -- 右フリッパーのヒンジ位置
    local rightPos = Vector3.new(tablePos.X + 20, y, tablePos.Z + 80)
    Flipper.right = createFlipper("RightFlipper", CFrame.new(rightPos), parent)
end

local function setTarget(flipper, isLeft, pressed)
    local target = pressed and FLIPPER_ANGLE or 0
    if isLeft then
        Flipper.leftTarget = target
    else
        Flipper.rightTarget = target
    end
end

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    if input.KeyCode == Enum.KeyCode.Left then
        setTarget(Flipper.left, true, true)
    elseif input.KeyCode == Enum.KeyCode.Right then
        setTarget(Flipper.right, false, true)
    end
end)

UserInputService.InputEnded:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    if input.KeyCode == Enum.KeyCode.Left then
        setTarget(Flipper.left, true, false)
    elseif input.KeyCode == Enum.KeyCode.Right then
        setTarget(Flipper.right, false, false)
    end
end)

-- 毎フレームでスムーズに回転させる
RunService.Heartbeat:Connect(function(dt)
    if Flipper.left then
        local current = Flipper.left.CFrame - Flipper.left.CFrame.p
        local targetRot = CFrame.Angles(0, 0, -Flipper.leftTarget)
        Flipper.left.CFrame = Flipper.left.CFrame:Lerp(Flipper.left.CFrame * targetRot, dt / FLIPPER_SPEED)
    end
    if Flipper.right then
        local targetRot = CFrame.Angles(0, 0, Flipper.rightTarget)
        Flipper.right.CFrame = Flipper.right.CFrame:Lerp(Flipper.right.CFrame * targetRot, dt / FLIPPER_SPEED)
    end
end)

return Flipper
