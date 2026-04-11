-- Table.lua: ピンボールのテーブルと壁、バンパーを作成するモジュール
local Table = {}

-- テーブルサイズ（幅, 奥行き, 高さ）
local TABLE_SIZE = Vector3.new(100, 5, 200)

-- 壁の厚さ
local WALL_THICKNESS = 2

-- バンパーの半径と高さ
local BUMPER_RADIUS = 5
local BUMPER_HEIGHT = 5

-- ユーティリティ: パーツ作成
local function createPart(name, size, position, parent, color)
    local part = Instance.new("Part")
    part.Name = name
    part.Size = size
    part.Position = position
    part.Anchored = true
    part.CanCollide = true
    part.Color = color or Color3.new(1, 1, 1)
    part.Parent = parent
    return part
end

function Table.create(parent)
    -- テーブル本体
    local tablePart = createPart("PinballTable", TABLE_SIZE, parent.Position, parent, Color3.fromRGB(30,30,30))

    local halfX = TABLE_SIZE.X/2
    local halfZ = TABLE_SIZE.Z/2
    local y = parent.Position.Y + TABLE_SIZE.Y/2

    -- 四方の壁を作成
    createPart("WallFront", Vector3.new(TABLE_SIZE.X, TABLE_SIZE.Y, WALL_THICKNESS), Vector3.new(parent.Position.X, y, parent.Position.Z - halfZ), parent, Color3.fromRGB(80,80,80))
    createPart("WallBack",  Vector3.new(TABLE_SIZE.X, TABLE_SIZE.Y, WALL_THICKNESS), Vector3.new(parent.Position.X, y, parent.Position.Z + halfZ), parent, Color3.fromRGB(80,80,80))
    createPart("WallLeft",  Vector3.new(WALL_THICKNESS, TABLE_SIZE.Y, TABLE_SIZE.Z), Vector3.new(parent.Position.X - halfX, y, parent.Position.Z), parent, Color3.fromRGB(80,80,80))
    createPart("WallRight", Vector3.new(WALL_THICKNESS, TABLE_SIZE.Y, TABLE_SIZE.Z), Vector3.new(parent.Position.X + halfX, y, parent.Position.Z), parent, Color3.fromRGB(80,80,80))

    -- バンパーをいくつか配置（例: 4 つ）
    local bumperPositions = {
        Vector3.new(parent.Position.X - 20, y + BUMPER_HEIGHT/2, parent.Position.Z - 30),
        Vector3.new(parent.Position.X + 20, y + BUMPER_HEIGHT/2, parent.Position.Z - 30),
        Vector3.new(parent.Position.X - 20, y + BUMPER_HEIGHT/2, parent.Position.Z + 30),
        Vector3.new(parent.Position.X + 20, y + BUMPER_HEIGHT/2, parent.Position.Z + 30),
    }
    for i, pos in ipairs(bumperPositions) do
        local bumper = Instance.new("Part")
        bumper.Name = "Bumper"..i
        bumper.Shape = Enum.PartType.Ball
        bumper.Size = Vector3.new(BUMPER_RADIUS*2, BUMPER_HEIGHT, BUMPER_RADIUS*2)
        bumper.Position = pos
        bumper.Anchored = true
        bumper.CanCollide = true
        bumper.Color = Color3.fromRGB(255, 100, 100)
        bumper.Parent = parent
    end
end

return Table
