-- Ball.lua: ピンボールのボールを生成し、衝突時にスコアを加算するモジュール
local Ball = {}

local BALL_RADIUS = 2
local BALL_COLOR = Color3.fromRGB(255, 255, 255)

local function createBall(parent)
    local ball = Instance.new("Part")
    ball.Name = "PinballBall"
    ball.Shape = Enum.PartType.Ball
    ball.Size = Vector3.new(BALL_RADIUS*2, BALL_RADIUS*2, BALL_RADIUS*2)
    ball.Position = parent.Position + Vector3.new(0, 10, 0) -- テーブル上に少し上げて配置
    ball.Color = BALL_COLOR
    ball.Material = Enum.Material.Neon
    ball.Anchored = false
    ball.CanCollide = true
    ball.BrickColor = BrickColor.new("Bright yellow")
    ball.Parent = parent
    return ball
end

function Ball.spawn(parent)
    local ball = createBall(parent)
    -- 初期速度（例: 前方へ）
    local bodyVelocity = Instance.new("BodyVelocity")
    bodyVelocity.Velocity = Vector3.new(0, 0, -30)
    bodyVelocity.MaxForce = Vector3.new(1e5, 1e5, 1e5)
    bodyVelocity.Parent = ball

    -- スコア加算ロジック（バンパーに触れたら ScoreManager に通知）
    ball.Touched:Connect(function(hit)
        if hit.Name:match("Bumper") then
            local scoreMgr = require(script.Parent.ScoreManager)
            scoreMgr.addScore(10)
        end
    end)
end

return Ball
