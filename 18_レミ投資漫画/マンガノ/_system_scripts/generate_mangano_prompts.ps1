$ErrorActionPreference = "Stop"

$BaseDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\マンガノ\01_長編_希望の投資"
if (-not (Test-Path $BaseDir)) { New-Item -Path $BaseDir -ItemType Directory -Force }

# Master Prompts
$MASTER_ARCHITECTURE = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17."
$CHAR_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
$CHAR_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS."
$CHAR_TANAKA = "- Tanaka: (Arrogant Japanese man, dark suit, loose tie). (Short messy brown hair). (Sneering smirk)."
$CHAR_ZOUZEI = "- Zouzei-man: (Massive monster made of tax forms and coins). (Glowing purple eyes)."
$CHAR_BUKKADAKA = "- Bukkadaka-man: (Bloated monster with red price tags). (Gaping sharp-toothed mouth)."
$CHAR_MONEYTREE = "- MoneyTree: (Radiant golden tree/sapling). (Golden light aura)."
$CHAR_NOISE = "- Noise: (Swirling black and purple mist with ghostly faces)."

$MASTER_STYLE = "### Style: Premium manga, cinematic lighting, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. FULL BLEED."
$MASTER_NEGATIVE = "**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped."

$HEADER = @"
$MASTER_ARCHITECTURE

### Characters:
$CHAR_REMI
$CHAR_YUTO
$CHAR_TANAKA
$CHAR_ZOUZEI
$CHAR_BUKKADAKA
$CHAR_MONEYTREE
$CHAR_NOISE

$MASTER_STYLE
$MASTER_NEGATIVE
"@

$Episodes = @(
    @{No = 1; Title = "絶望の現代社会"; Range = "P1-5"; Desc = "増税マン・物価高マンの襲来と、優斗の経済的困窮。" },
    @{No = 2; Title = "搾取の連鎖"; Range = "P6-10"; Desc = "手取りへの攻撃と、同僚田中のFX自慢。" },
    @{No = 3; Title = "甘い誘惑"; Range = "P11-15"; Desc = "田中の豪遊と優斗の焦り。レバレッジの誘惑。" },
    @{No = 4; Title = "救世主レミ"; Range = "P16-20"; Desc = "公園での運命の出会い。波動の乱れの指摘。" },
    @{No = 5; Title = "カメの歩み"; Range = "P21-25"; Desc = "レミによる投資教育開始。投機と投資の違い。" },
    @{No = 6; Title = "複利の魔法"; Range = "P26-30"; Desc = "宇宙最強の力、複利の視覚化。" },
    @{No = 7; Title = "苗木を植える"; Range = "P31-35"; Desc = "金のなる木の苗木を植える精神的儀式。" },
    @{No = 8; Title = "積立の開始"; Range = "P36-40"; Desc = "S&P500への入金。田中の冷笑。" },
    @{No = 9; Title = "嵐の予兆"; Range = "P41-45"; Desc = "数年後。順調な成長と田中の異常な膨張。" },
    @{No = 10; Title = "ブラック・スワン"; Range = "P46-50"; Desc = "暴落の発生。ノイズが世界を覆う。" },
    @{No = 11; Title = "田中の退場"; Range = "P51-55"; Desc = "ロスカットに泣く田中。投機の残酷さ。" },
    @{No = 12; Title = "握力の試練"; Range = "P56-60"; Desc = "苗木を引き抜こうとする優斗をレミが制止。" },
    @{No = 13; Title = "静かなる忍耐"; Range = "P61-65"; Desc = "レミの結界の中での沈黙。再上昇の兆し。" },
    @{No = 14; Title = "再生の緑"; Range = "P66-70"; Desc = "株価回復。苗木が以前より太くなる。" },
    @{No = 15; Title = "最初の果実"; Range = "P71-75"; Desc = "初めての配当。再投資の喜び。" },
    @{No = 16; Title = "落差の現実"; Range = "P76-80"; Desc = "リベンジFXでさらに沈む田中との対比。" },
    @{No = 17; Title = "資産の盾"; Range = "P81-85"; Desc = "資産という名のシールド。経済的防御の完成。" },
    @{No = 18; Title = "黄金の波動"; Range = "P86-90"; Desc = "精神的自立。レミが優斗の成長を認める。" },
    @{No = 19; Title = "20年後の朝"; Range = "P91-95"; Desc = "大樹となった資産。自由な時間の獲得。" },
    @{No = 20; Title = "F-U Money"; Range = "P96-100"; Desc = "嫌なことにNOと言える力。後輩への伝承。" },
    @{No = 21; Title = "お金の旅路"; Range = "P101-105"; Desc = "レミとの対話。お金は手段であること。" },
    @{No = 22; Title = "自分自身の道"; Range = "P106-110"; Desc = "夢への再挑戦。真の豊かさ。" },
    @{No = 23; Title = "希望の投資"; Range = "P111-115"; Desc = "エピローグ。次世代へ繋ぐバトン。" }
)

foreach ($Ep in $Episodes) {
    $FileName = "No102_{0:D2}_{1}_{2}_プロンプト.md" -f $Ep.No, $Ep.Title, $Ep.Range
    $FilePath = Join-Path $BaseDir $FileName
    
    $PagesText = ""
    $StartPage = [int]($Ep.Range -replace "P(\d+)-.*", '$1')
    $EndPage = [int]($Ep.Range -replace ".*-(\d+)", '$1')
    
    for ($p = $StartPage; $p -le $EndPage; $p++) {
        $PagesText += @"
---

## $p ページ目プロンプト (v15.5 Edge Obliterator)

``javascript
generate_image(
  ImageName: "remi_102_ep$($Ep.No)_p$($p)_final",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 12:17.
Characters: {Remi}, {Yuto}, {Tanaka}, {Villains}.
[PANEL 1 - 40% height]: FULL WIDTH FILL. $($Ep.Desc). Detailed 2D anime style.
[PANEL 2 - 35% height]: FULL WIDTH FILL. Interaction in $($Ep.Title). Blank speech bubbles.
[PANEL 3 - 25% height]: FULL WIDTH FILL. Symbolic background. Cinematic lighting.
"
)
``

"@
    }

    $Content = @"
# No102 Episode $($Ep.No): $($Ep.Title) ($($Ep.Range))

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| EP | $($Ep.No) |
| タイトル | $($Ep.Title) |
| 解説 | $($Ep.Desc) |

---

$PagesText

作成日: $(Get-Date -Format "yyyy-MM-dd")
ステータス: $($Ep.Range) v15.5 Edge Obliterator 完備
"@

    # Handle backticks for code block in content
    $Content = $Content -replace "``javascript", "```javascript"
    $Content = $Content -replace "``", "```"

    Set-Content -Path $FilePath -Value $Content -Encoding UTF8
    Write-Host "Generated: $FileName"
}
