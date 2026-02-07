$ErrorActionPreference = "Stop"

$BaseDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\102プロンプト\01_長編_希望の投資"

$MASTER_ARCHITECTURE = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17."
$MASTER_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES."
$MASTER_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS."
$MASTER_STYLE = "### Style: Premium manga, cinematic lighting, best quality, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. ALL ART MUST BE FULL BLEED."
$MASTER_NEGATIVE = "**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped."

$HEADER_TEMPLATE = @"
$MASTER_ARCHITECTURE

### Characters:
$MASTER_REMI
$MASTER_YUTO
- Tanaka: (Dark suit, loose tie, arrogant smirk). (Short messy brown hair).
- Zouzei-man: (Giant monstrous figure made of tax forms and coins). (Dark shadowy aura).
- Bukkadaka-man: (Bloated monster with price tags). (Red angry aura).
- MoneyTree: (Glowing golden sapling/tree). (Radiant energy).

$MASTER_STYLE
$MASTER_NEGATIVE

"@

$Chapters = @(
    @{Num = 1; Title = "絶望と誘惑"; Start = 1; End = 20; Desc = "増税マン・物価高マンの襲撃、田中の誘惑" },
    @{Num = 2; Title = "種を蒔く決意"; Start = 21; End = 40; Desc = "レミの説教、複利の魔法、苗木を植える" },
    @{Num = 3; Title = "嵐と試練"; Start = 41; End = 65; Desc = "暴落、ノイズ、田中の退場、耐える優斗" },
    @{Num = 4; Title = "成長と開花"; Start = 66; End = 90; Desc = "資産回復、金のなる木の成長、精神的自立" },
    @{Num = 5; Title = "未来への継承"; Start = 91; End = 115; Desc = "20年後、F-U Money、後輩への指導、エピローグ" }
)

$FileCounter = 1

foreach ($Chap in $Chapters) {
    $Pages = $Chap.Start..$Chap.End
    
    # Chunk pages
    for ($i = 0; $i -lt $Pages.Count; $i += 3) {
        $Chunk = $Pages[$i..($i + 2)]
        $CurrentPages = $Chunk | Where-Object { $_ -ne $null }
        
        # Pad if less than 3
        while ($CurrentPages.Count -lt 3) {
            $CurrentPages += $CurrentPages[-1]
        }
        
        $PStart = $CurrentPages[0]
        # $PEnd skipped as it was unused and causing warnings
        
        # Fix PEnd for display if it was padded
        if ($i + 2 -ge $Pages.Count) {
            $RealEnd = $Pages[-1]
        }
        else {
            $RealEnd = $Pages[$i + 2]
        }
        
        if ($PStart -eq $RealEnd) {
            $FileName = "No102_{0:D3}_Ch{1}_P{2:D3}_プロンプト.md" -f $FileCounter, $Chap.Num, $PStart
            $DisplayTitle = "第{0}章 {1} (P{2})" -f $Chap.Num, $Chap.Title, $PStart
        }
        else {
            $FileName = "No102_{0:D3}_Ch{1}_P{2:D3}-{3:D3}_プロンプト.md" -f $FileCounter, $Chap.Num, $PStart, $RealEnd
            $DisplayTitle = "第{0}章 {1} (P{2}-{3})" -f $Chap.Num, $Chap.Title, $PStart, $RealEnd
        }

        $SceneDesc = $Chap.Desc

        $Content = $HEADER_TEMPLATE + @"
# Page $($CurrentPages[0])
[Panel 1]: High quality manga panel. $SceneDesc. Focus on emotion and atmosphere. Masterpiece.
[Panel 2]: High quality manga panel. Character interaction. $SceneDesc. Detailed background.
[Panel 3]: High quality manga panel. Dramatic angle. $SceneDesc. 12:17 vertical ratio.

# Page $($CurrentPages[1])
[Panel 1]: High quality manga panel. $SceneDesc. Progressing story.
[Panel 2]: High quality manga panel. $SceneDesc. Emotional reaction.
[Panel 3]: High quality manga panel. $SceneDesc. Symbolic imagery.

# Page $($CurrentPages[2])
[Panel 1]: High quality manga panel. $SceneDesc. Climax of the sequence.
[Panel 2]: High quality manga panel. $SceneDesc. Reflective moment.
[Panel 3]: High quality manga panel. $SceneDesc. Transition to next scene.

| タイトル | $DisplayTitle |
| 解説 | $SceneDesc |
"@

        $FilePath = Join-Path $BaseDir $FileName
        Set-Content -Path $FilePath -Value $Content -Encoding UTF8
        Write-Host "Created: $FileName"
        
        $FileCounter++
    }
}
