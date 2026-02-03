<#
.SYNOPSIS
    レミの兵法投資 - プロンプト一括生成スクリプト

.DESCRIPTION
    101個のTIPに対応するプロンプトファイルを各テーマフォルダに生成します。
    - データ定義とテンプレート生成を分離
    - 再実行可能（既存ファイルは上書き）

.NOTES
    作成日: 2026-02-03
    バージョン: 2.0
#>

#region 設定

$Config = @{
    BasePath   = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"
    Categories = @{
        1 = "01_投資の基礎知識"
        2 = "02_マインド・哲学"
        3 = "03_戦略・リスク管理"
        4 = "04_未来・テクノロジー"
    }
}

#endregion

#region TIPデータ定義

# カテゴリー1: 投資の基礎知識 (No.1-25)
$Category1 = @(
    @{No = 2; Title = "複利"; Desc = "利益が利益を生む魔法。雪だるま式に増える。" }
    @{No = 3; Title = "長期投資"; Desc = "数年から数十年保有する手法。時間を味方につける。" }
    @{No = 4; Title = "ドルコスト平均法"; Desc = "定期定額購入。高い時は少なく安い時は多く買う。" }
    @{No = 5; Title = "逆張り"; Desc = "株価暴落時にあえて買う手法。" }
    @{No = 6; Title = "織り込み済み"; Desc = "ニュースや予測は既に株価に反映されている。" }
    @{No = 7; Title = "一番は死んだ人"; Desc = "運用成績が最も良いのは放置された口座。" }
    @{No = 8; Title = "管理すること"; Desc = "スプレッドシートなどで資産状況を可視化する。" }
    @{No = 9; Title = "お金の価値は下がる"; Desc = "インフレで現金の価値は下がる。" }
    @{No = 10; Title = "今後の増税計画"; Desc = "手取りは減る一方。増やすスキルが必須。" }
    @{No = 11; Title = "防衛費とミサイル"; Desc = "国際情勢と予算の関係。社会の裏側を読む。" }
    @{No = 12; Title = "名言エピソード"; Desc = "投資の格言には先人の知恵が詰まっている。" }
    @{No = 13; Title = "メタ認知"; Desc = "自分を客観視する。パニック時に気づく力。" }
    @{No = 14; Title = "家計の見直し"; Desc = "保険や携帯など。無駄な固定費を削減。" }
    @{No = 15; Title = "マインドセット"; Desc = "心が一番大事。テクニックよりメンタル。" }
    @{No = 16; Title = "五公五民"; Desc = "サラリーマンの実質税負担率は高い。" }
    @{No = 17; Title = "1割貯蓄3割投資"; Desc = "給料の一定割合を天引きして投資へ。" }
    @{No = 18; Title = "NISA枠"; Desc = "年間360万円の非課税枠を活用する。" }
    @{No = 19; Title = "お金の勉強の欠如"; Desc = "学校では教えてくれない。自分で学ぶ。" }
    @{No = 20; Title = "未来年表"; Desc = "世界人口やテクノロジーの進化を予測する。" }
    @{No = 21; Title = "分散投資"; Desc = "卵を一つのカゴに盛るな。リスクを分ける。" }
    @{No = 22; Title = "口座の種類"; Desc = "特定口座が楽。一般口座は確定申告が必要。" }
    @{No = 23; Title = "仮想通貨"; Desc = "株とは違う動き。市場心理がダイレクトに反映。" }
    @{No = 24; Title = "PayPay証券"; Desc = "1000円から少額で米国株が買える。" }
    @{No = 25; Title = "ETF"; Desc = "上場投資信託。株の詰め合わせパック。" }
)

# カテゴリー2: マインド・哲学 (No.26-50)
$Category2 = @(
    @{No = 26; Title = "毎月配当"; Desc = "毎月お小遣いが入る喜び。" }
    @{No = 27; Title = "テスラ"; Desc = "革新的な企業の代表例。夢を買う。" }
    @{No = 28; Title = "インカムvsキャピタル"; Desc = "配当狙いか値上がり狙いか。" }
    @{No = 29; Title = "筋トレと健康"; Desc = "お金があっても健康でなければ意味がない。" }
    @{No = 30; Title = "明日あくる日"; Desc = "明るい日と書いて明日。未来は自分次第。" }
    @{No = 31; Title = "老後の年金"; Desc = "平均月額では生きられない現実。" }
    @{No = 32; Title = "ESBI"; Desc = "金持ち父さんの4つのクワドラント。" }
    @{No = 33; Title = "成長投資"; Desc = "これから伸びる企業への投資。" }
    @{No = 34; Title = "一般投資"; Desc = "堅実な投資。" }
    @{No = 35; Title = "株の始まり"; Desc = "大航海時代。船のリスク分散から始まった。" }
    @{No = 36; Title = "損切り"; Desc = "失敗を認めて傷を浅く済ませる技術。" }
    @{No = 37; Title = "塩漬け"; Desc = "含み損で売れなくなった状態。" }
    @{No = 38; Title = "PBR"; Desc = "株価純資産倍率。割安かどうかの指標。" }
    @{No = 39; Title = "AIロボット"; Desc = "次の産業革命。労働からの解放か。" }
    @{No = 40; Title = "逆張り2"; Desc = "みんなが恐怖している時に買う勇気。" }
    @{No = 41; Title = "FIRE"; Desc = "経済的自立と早期リタイア。配当生活。" }
    @{No = 42; Title = "足るを知る"; Desc = "現状に感謝する心。欲望にはキリがない。" }
    @{No = 43; Title = "不況と富豪"; Desc = "富豪は不況で生まれる。暴落こそチャンス。" }
    @{No = 44; Title = "オキシトシン的成功"; Desc = "つながりの幸福。家族やパートナー。" }
    @{No = 45; Title = "セロトニン的成功"; Desc = "健康の幸福。心身の安定が土台。" }
    @{No = 46; Title = "死ぬ時の後悔"; Desc = "もっと挑戦すればよかった。" }
    @{No = 47; Title = "逆算思考"; Desc = "ゴールから考えて今やるべきことを決める。" }
    @{No = 48; Title = "72の法則"; Desc = "資産が2倍になる年数は72を年利で割る。" }
    @{No = 49; Title = "年金の手取り"; Desc = "額面と手取りは違う。税金が引かれる。" }
    @{No = 50; Title = "大暴落"; Desc = "戻らない暴落はない。歴史が証明している。" }
)

# カテゴリー3: 戦略・リスク管理 (No.51-75)
$Category3 = @(
    @{No = 51; Title = "損切りと逆張り"; Desc = "適切な損切りが次のチャンスの資金を生む。" }
    @{No = 52; Title = "急ぐな"; Desc = "急いで金持ちになろうとするな。" }
    @{No = 53; Title = "複利再"; Desc = "時間をかけるほど強大になる。" }
    @{No = 54; Title = "長期マラソン"; Desc = "10年20年単位の勝負。一喜一憂しない。" }
    @{No = 55; Title = "変えられないもの"; Desc = "過去と他人は変えられない。" }
    @{No = 56; Title = "失敗は経験"; Desc = "うまくいかない方法を発見しただけ。" }
    @{No = 57; Title = "向上心"; Desc = "ありのままで良いが努力を忘れない。" }
    @{No = 58; Title = "固定費削減"; Desc = "携帯代やサブスク。質素倹約が大事。" }
    @{No = 59; Title = "証券会社比較"; Desc = "楽天やSBIなど。使いやすさで選ぶ。" }
    @{No = 60; Title = "死ぬ時の後悔Top10"; Desc = "多くの人が同じことを後悔する。" }
    @{No = 61; Title = "手段と目的"; Desc = "お金は手段。目的は幸せや自由。" }
    @{No = 62; Title = "ピケティ"; Desc = "21世紀の資本。格差は広がり続ける。" }
    @{No = 63; Title = "rとg"; Desc = "資本収益率が経済成長率を上回る。" }
    @{No = 64; Title = "スピリチュアル"; Desc = "直感や運も大事にする。" }
    @{No = 65; Title = "金利比較"; Desc = "銀行預金vs株式配当。その差は数千倍。" }
    @{No = 66; Title = "今日が一番若い"; Desc = "始めるなら今がベストタイミング。" }
    @{No = 67; Title = "長期vs短期"; Desc = "目先の利益より将来の大きな果実。" }
    @{No = 68; Title = "失敗と学び"; Desc = "失敗から何を学ぶかが重要。" }
    @{No = 69; Title = "投資仲間"; Desc = "孤独にならない。情報共有し励まし合う。" }
    @{No = 70; Title = "嫉妬vs祝福"; Desc = "他人の成功を喜べるか。" }
    @{No = 71; Title = "自己投資"; Desc = "最もリターンの高い投資は自分自身への投資。" }
    @{No = 72; Title = "バランス"; Desc = "金と健康と人間関係。どれも大事。" }
    @{No = 73; Title = "権利確定日"; Desc = "この日に株を持っていないと配当はもらえない。" }
    @{No = 74; Title = "株主優待"; Desc = "日本独自の文化。商品やサービス券がもらえる。" }
    @{No = 75; Title = "ジャーナリング"; Desc = "書く瞑想。思考を紙に書き出して整理する。" }
)

# カテゴリー4: 未来・テクノロジー (No.76-101)
$Category4 = @(
    @{No = 76; Title = "リテラシー"; Desc = "日本は金融リテラシーが低い。" }
    @{No = 77; Title = "海外の教育"; Desc = "海外では子供の頃からお金の授業がある。" }
    @{No = 78; Title = "感情のコントロール"; Desc = "興奮や恐怖で売買しない。" }
    @{No = 79; Title = "ストップ高安"; Desc = "日本株の値幅制限。行き過ぎを止める。" }
    @{No = 80; Title = "管理再"; Desc = "スプレッドシート等で資産を可視化し続ける。" }
    @{No = 81; Title = "81番"; Desc = "投資の基本を忘れずに。" }
    @{No = 82; Title = "毎月配当再"; Desc = "インカムゲインの積み上げがFIREへの道。" }
    @{No = 83; Title = "ETF再"; Desc = "個別株より低リスク。初心者の最適解。" }
    @{No = 84; Title = "Grokで銘柄探し"; Desc = "AIを活用して有望銘柄を見つける。" }
    @{No = 85; Title = "ChatGPT壁打ち"; Desc = "投資判断の相談相手としてAIを使う。" }
    @{No = 86; Title = "お金と平穏"; Desc = "枕を高くして眠れる投資をする。" }
    @{No = 87; Title = "カルダシェフ尺度"; Desc = "文明の進化レベル。人類はまだタイプ0。" }
    @{No = 88; Title = "脳内チップ"; Desc = "ニューラリンク。人間とAIの融合。" }
    @{No = 89; Title = "宇宙太陽光"; Desc = "無限のエネルギー。新しい産業。" }
    @{No = 90; Title = "連想ゲーム"; Desc = "ニュースから関連銘柄を探す。" }
    @{No = 91; Title = "ピケティ再"; Desc = "富の集中は加速する。投資側に回る。" }
    @{No = 92; Title = "孫子の兵法"; Desc = "負けないことが大事。生き残ればチャンスは来る。" }
    @{No = 93; Title = "100年単位"; Desc = "人生100年時代。超長期視点で考える。" }
    @{No = 94; Title = "致命傷を避ける"; Desc = "再起不能な損失だけは避ける。" }
    @{No = 95; Title = "虎穴に入らずんば"; Desc = "リスクを取らなければリターンは得られない。" }
    @{No = 96; Title = "長期のメリット"; Desc = "複利効果やストレス減や税金繰り延べ効果。" }
    @{No = 97; Title = "デイトレ"; Desc = "専業の世界。修羅の道。" }
    @{No = 98; Title = "平均取得単価"; Desc = "ナンピン買いで単価を下げる技術。" }
    @{No = 99; Title = "損切り再"; Desc = "サンクコストバイアスを捨てる。" }
    @{No = 100; Title = "戻る暴落"; Desc = "世界経済は右肩上がり。信じて待つ。" }
    @{No = 101; Title = "確率論"; Desc = "試行回数を増やす。分散投資。" }
)

# 全TIPデータを統合
$AllTips = @{
    1 = $Category1
    2 = $Category2
    3 = $Category3
    4 = $Category4
}

#endregion

#region ヘルパー関数

function Get-SafeFileName {
    <#
    .SYNOPSIS
        ファイル名として使用できない文字を除去
    #>
    param([string]$Name)
    return $Name -replace '[\\/:*?"<>|]', ''
}

function New-CategoryFolder {
    <#
    .SYNOPSIS
        カテゴリフォルダが存在しない場合は作成
    #>
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "  [フォルダ作成] $Path" -ForegroundColor Blue
    }
}

#endregion

#region テンプレート生成

function New-PromptTemplate {
    <#
    .SYNOPSIS
        プロンプトファイルの内容を生成
    #>
    param(
        [int]$No,
        [string]$Title,
        [string]$Description,
        [string]$Category
    )
    
    $noStr = $No.ToString("D2")
    $safeTitle = Get-SafeFileName -Name $Title
    $date = Get-Date -Format "yyyy-MM-dd"
    
    # テンプレート行を配列で構築
    $lines = @(
        "# No.$No $Title 2P漫画生成プロンプト"
        ""
        "## TIP情報"
        ""
        "| 項目     | 内容                |"
        "| -------- | ------------------- |"
        "| No       | $No                 |"
        "| タイトル | $Title              |"
        "| 解説     | $Description        |"
        "| カテゴリ | $Category           |"
        ""
        "---"
        ""
        "## 1ページ目プロンプト"
        ""
        "~~~text"
        "[OUTPUT: 1200x1700 pixels, aspect ratio 12:17, portrait orientation]"
        ""
        "MANDATORY IMAGE SPECIFICATIONS:"
        "- Canvas Size: 1200 pixels width x 1700 pixels height"
        "- Aspect Ratio: 12:17 (portrait)"
        "- Resolution: High quality manga illustration"
        ""
        "PANEL LAYOUT - PAGE 1:"
        "- Panel 1 (TOP 40%): Large horizontal panel"
        "- Panel 2 (MIDDLE 30%): Medium horizontal panel"
        "- Panel 3 (BOTTOM-LEFT 15%): Small vertical panel"
        "- Panel 4 (BOTTOM-RIGHT 15%): Small vertical panel"
        ""
        "TEXT BOX in Panel 1 BOTTOM-RIGHT: Black box with white text: テーマ $Title"
        ""
        "STYLE: Japanese manga, 6500K white balance, cel shading, white speech bubbles"
        ""
        "IMPORTANT: DO NOT render character names in speech bubbles"
        ""
        "Panel 1 - Introduction:"
        "Scene: Modern office with city view, afternoon sunlight"
        "Characters:"
        "- Boy: Black GAKURAN uniform, gold buttons, short black hair, curious expression"
        "- Woman: Silver hair, red eyes, red blazer, black lace top, confident smile"
        "Speech bubble: 姉さん $Title について教えてください"
        ""
        "Panel 2 - Explanation:"
        "Scene: Close-up of silver-haired woman explaining"
        "Speech bubble: $Description"
        ""
        "Panel 3 - Reaction:"
        "Scene: Boy surprised face"
        "Speech bubble: なるほど"
        ""
        "Panel 4 - Conclusion:"
        "Scene: Woman with mysterious smile"
        "Speech bubble: これが投資の真実よ"
        "~~~"
        ""
        "---"
        ""
        "## 2ページ目プロンプト"
        ""
        "~~~text"
        "[OUTPUT: 1200x1700 pixels, aspect ratio 12:17, portrait orientation]"
        ""
        "MANDATORY IMAGE SPECIFICATIONS:"
        "- Canvas Size: 1200 pixels width x 1700 pixels height"
        "- Aspect Ratio: 12:17 (portrait)"
        ""
        "PANEL LAYOUT - PAGE 2:"
        "- Panel 1 (TOP 50%): Large cinematic panel"
        "- Panel 2 (MIDDLE-LEFT 25%): Vertical panel"
        "- Panel 3 (MIDDLE-RIGHT 25%): Vertical panel"
        "- Panel 4 (BOTTOM 25%): Wide conclusion panel"
        ""
        "IMPORTANT: DO NOT render character names in speech bubbles"
        ""
        "Panel 1 - Visual Metaphor:"
        "Scene: Dramatic visualization of $Title concept"
        "Narration: $Description"
        ""
        "Panel 2 - Point 1:"
        "Narration: ポイント1"
        ""
        "Panel 3 - Point 2:"
        "Narration: ポイント2"
        ""
        "Panel 4 - Ending:"
        "Scene: Both characters in office, satisfied expressions"
        "Speech bubbles:"
        "勉強になりました 実践してみます"
        "その意気よ 一歩一歩 着実にね"
        "~~~"
        ""
        "---"
        ""
        "## 保存ファイル名"
        ""
        "- 1ページ目: No${noStr}_${safeTitle}_p1.png"
        "- 2ページ目: No${noStr}_${safeTitle}_p2.png"
        ""
        "---"
        ""
        "作成日: $date"
    )
    
    return $lines -join "`r`n"
}

#endregion

#region メイン処理

function Start-PromptGeneration {
    <#
    .SYNOPSIS
        プロンプトファイル一括生成のメイン処理
    #>
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " プロンプトファイル一括生成" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $totalCreated = 0
    $totalSkipped = 0
    
    foreach ($catKey in $AllTips.Keys | Sort-Object) {
        $categoryName = $Config.Categories[$catKey]
        $categoryPath = Join-Path $Config.BasePath $categoryName
        $tips = $AllTips[$catKey]
        
        Write-Host "[$categoryName]" -ForegroundColor Yellow
        New-CategoryFolder -Path $categoryPath
        
        foreach ($tip in $tips) {
            $noStr = $tip.No.ToString("D2")
            $safeTitle = Get-SafeFileName -Name $tip.Title
            $fileName = "No${noStr}_${safeTitle}_プロンプト.md"
            $filePath = Join-Path $categoryPath $fileName
            
            # テンプレート生成
            $content = New-PromptTemplate `
                -No $tip.No `
                -Title $tip.Title `
                -Description $tip.Desc `
                -Category $categoryName
            
            # ファイル出力
            $content | Out-File -FilePath $filePath -Encoding UTF8 -Force
            Write-Host "  + $fileName" -ForegroundColor Green
            $totalCreated++
        }
        
        Write-Host ""
    }
    
    # サマリー表示
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " 完了" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  生成ファイル数: $totalCreated" -ForegroundColor Green
    Write-Host ""
}

#endregion

# 実行
Start-PromptGeneration
