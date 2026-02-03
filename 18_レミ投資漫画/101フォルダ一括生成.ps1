# レミの兵法投資 - 101個のフォルダとプロンプト一括生成スクリプト
# 作成日: 2026-02-03

$baseDir = "c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# TIPデータ（リストから抽出）
$tips = @(
    @{No = 1; Title = "配当貴族"; Content = "S&P500指数の中で25年以上連続増配している優良銘柄。信頼の証。"; Category = "基礎知識" },
    @{No = 2; Title = "複利"; Content = "利益が利益を生む魔法。「人類最大の発見」（アインシュタイン）。雪だるま式に増える。"; Category = "基礎知識" },
    @{No = 3; Title = "長期投資"; Content = "数年〜数十年保有する手法。時間を味方につけ、リスクを均す。マラソンと同じ。"; Category = "基礎知識" },
    @{No = 4; Title = "ドルコスト平均法"; Content = "定期定額購入。高い時は少なく、安い時は多く買うことで平均単価を下げる。"; Category = "基礎知識" },
    @{No = 5; Title = "逆張り"; Content = "株価暴落時（20%超下落など）にあえて買う手法。「人の行く裏に道あり花の山」。"; Category = "基礎知識" },
    @{No = 6; Title = "織り込み済み"; Content = "すでにそのニュースや予測は株価に反映されているということ。"; Category = "基礎知識" },
    @{No = 7; Title = "一番は死んだ人"; Content = "運用成績が最も良いのは「亡くなって放置されていた口座」＝いじらないのが最強。"; Category = "基礎知識" },
    @{No = 8; Title = "管理すること"; Content = "スプレッドシートなどで資産状況を可視化すること。"; Category = "基礎知識" },
    @{No = 9; Title = "お金の価値は下がる"; Content = "インフレ。昔のジュース100円→今120円。現金で持つリスク。"; Category = "基礎知識" },
    @{No = 10; Title = "今後の増税計画"; Content = "手取りは減る一方。だからこそ「増やすスキル」が必須。"; Category = "基礎知識" },
    @{No = 11; Title = "防衛費とミサイル"; Content = "国際情勢と予算の関係。社会の裏側を読む視点。"; Category = "基礎知識" },
    @{No = 12; Title = "名言エピソード"; Content = "投資の格言には先人の知恵が詰まっている。"; Category = "基礎知識" },
    @{No = 13; Title = "メタ認知"; Content = "自分を客観視する。暴落時にパニックになっている自分に気づく力。"; Category = "基礎知識" },
    @{No = 14; Title = "家計の見直し"; Content = "保険、携帯など。海外の富豪ほど無駄な固定費を使わない。"; Category = "基礎知識" },
    @{No = 15; Title = "マインドセット"; Content = "心（メンタル）が一番大事。テクニックよりメンタル。"; Category = "基礎知識" },
    @{No = 16; Title = "五公五民"; Content = "サラリーマンの実質税負担率は高い。江戸時代の一揆レベル。"; Category = "基礎知識" },
    @{No = 17; Title = "1割貯蓄・3割投資"; Content = "給料の一定割合を必ず天引きして投資へ。"; Category = "基礎知識" },
    @{No = 18; Title = "NISA枠"; Content = "年間360万円の非課税枠。これを使わない手はない。"; Category = "基礎知識" },
    @{No = 19; Title = "お金の勉強の欠如"; Content = "学校では教えてくれない。自分で学ぶしかない。"; Category = "基礎知識" },
    @{No = 20; Title = "未来年表"; Content = "今後の世界人口、テクノロジーの進化などを予測する。"; Category = "基礎知識" },
    @{No = 21; Title = "分散投資"; Content = "「卵を一つのカゴに盛るな」。リスクを分ける。"; Category = "基礎知識" },
    @{No = 22; Title = "口座の種類"; Content = "特定口座（源泉徴収あり）が楽。一般口座は確定申告が必要。"; Category = "基礎知識" },
    @{No = 23; Title = "仮想通貨"; Content = "株とは違う動き。市場心理がダイレクトに反映される。"; Category = "基礎知識" },
    @{No = 24; Title = "PayPay証券"; Content = "1000円から少額で米国株が買える。初心者向け。"; Category = "基礎知識" },
    @{No = 25; Title = "ETF"; Content = "上場投資信託。「株の詰め合わせパック」。"; Category = "基礎知識" },
    @{No = 26; Title = "毎月配当"; Content = "毎月お小遣いが入る喜び。モチベーション維持に効く。"; Category = "マインド" },
    @{No = 27; Title = "テスラ"; Content = "革新的な企業の代表例。夢を買う。"; Category = "マインド" },
    @{No = 28; Title = "インカム vs キャピタル"; Content = "配当（インカム）狙いか、値上がり（キャピタル）狙いか。"; Category = "マインド" },
    @{No = 29; Title = "筋トレと健康"; Content = "お金があっても健康でなければ意味がない。「健康 ＞ お金」。"; Category = "マインド" },
    @{No = 30; Title = "明日・あくる日"; Content = "明るい日と書いて明日。未来をどうするかは自分次第。"; Category = "マインド" },
    @{No = 31; Title = "老後の年金"; Content = "平均月額では生きられない現実。自助努力が必要。"; Category = "マインド" },
    @{No = 32; Title = "ESBI"; Content = "金持ち父さんの4つのクワドラント。労働収入から権利収入へ。"; Category = "マインド" },
    @{No = 33; Title = "成長投資"; Content = "これから伸びる企業・業界への投資。"; Category = "マインド" },
    @{No = 34; Title = "一般投資"; Content = "堅実な投資。"; Category = "マインド" },
    @{No = 35; Title = "株の始まり"; Content = "大航海時代。船のリスク分散から始まった仕組み。"; Category = "マインド" },
    @{No = 36; Title = "損切り"; Content = "失敗を認めて傷を浅く済ませる技術。"; Category = "マインド" },
    @{No = 37; Title = "塩漬け"; Content = "含み損で売るに売れなくなった状態。資金が拘束される。"; Category = "マインド" },
    @{No = 38; Title = "PBR"; Content = "株価純資産倍率。割安かどうかの指標。1倍割れはお買い得？"; Category = "マインド" },
    @{No = 39; Title = "AI × ロボット"; Content = "次の産業革命。労働からの解放？"; Category = "マインド" },
    @{No = 40; Title = "逆張り(2)"; Content = "みんなが恐怖している時に買う勇気。"; Category = "マインド" },
    @{No = 41; Title = "FIRE"; Content = "経済的自立と早期リタイア。配当生活。"; Category = "マインド" },
    @{No = 42; Title = "足るを知る"; Content = "現状に感謝する心。欲望にはキリがない。"; Category = "マインド" },
    @{No = 43; Title = "不況と富豪"; Content = "「富豪は不況で生まれる」。暴落こそチャンス。"; Category = "マインド" },
    @{No = 44; Title = "オキシトシン的成功"; Content = "「つながり」の幸福。家族、パートナー、ペット。"; Category = "マインド" },
    @{No = 45; Title = "セロトニン的成功"; Content = "「健康」の幸福。心身の安定。これが土台。"; Category = "マインド" },
    @{No = 46; Title = "死ぬ時の後悔"; Content = "「もっと挑戦すればよかった」「働きすぎなければよかった」。"; Category = "マインド" },
    @{No = 47; Title = "逆算思考"; Content = "ゴール（死、老後）から考えて今やるべきことを決める。"; Category = "マインド" },
    @{No = 48; Title = "72の法則"; Content = "資産が2倍になる年数 = 72 ÷ 年利。"; Category = "マインド" },
    @{No = 49; Title = "年金の手取り"; Content = "額面と手取りは違う。税金や社会保険料が引かれる。"; Category = "マインド" },
    @{No = 50; Title = "大暴落"; Content = "「戻らない暴落はない」。歴史が証明している。"; Category = "マインド" },
    @{No = 51; Title = "損切りと逆張り"; Content = "適切な損切りが、次の逆張りチャンスの資金を生む。"; Category = "戦略" },
    @{No = 52; Title = "急ぐな"; Content = "「急いで金持ちになろうとするな」。ウォーレン・バフェット。"; Category = "戦略" },
    @{No = 53; Title = "複利(再)"; Content = "アインシュタインの言葉。時間をかけるほど強大になる。"; Category = "戦略" },
    @{No = 54; Title = "長期マラソン"; Content = "10年、20年単位の勝負。短期の上下に一喜一憂しない。"; Category = "戦略" },
    @{No = 55; Title = "変えられないもの"; Content = "過去と他人は変えられない。未来と自分は変えられる。"; Category = "戦略" },
    @{No = 56; Title = "失敗は経験"; Content = "失敗ではなく、うまくいかない方法を発見しただけ。"; Category = "戦略" },
    @{No = 57; Title = "向上心"; Content = "ありのままで良いが、より良くなる努力を忘れない。"; Category = "戦略" },
    @{No = 58; Title = "固定費削減"; Content = "携帯代、サブスク。米国の富豪は質素倹約家が多い。"; Category = "戦略" },
    @{No = 59; Title = "証券会社比較"; Content = "楽天、SBIなど。使いやすさやポイントで選ぶ。"; Category = "戦略" },
    @{No = 60; Title = "死ぬ時の後悔Top10"; Content = "多くの人が同じことを後悔する。先人の教訓。"; Category = "戦略" },
    @{No = 61; Title = "手段と目的"; Content = "お金は「手段」。目的は「幸せ」「自由」「安心」。"; Category = "戦略" },
    @{No = 62; Title = "ピケティ"; Content = "『21世紀の資本』。格差は広がり続ける。"; Category = "戦略" },
    @{No = 63; Title = "r > g"; Content = "資本収益率(r) ＞ 経済成長率(g)。働くだけでは豊かになれない。"; Category = "戦略" },
    @{No = 64; Title = "スピリチュアル"; Content = "時には直感や運、目に見えない流れも大事にする。"; Category = "戦略" },
    @{No = 65; Title = "金利比較"; Content = "銀行預金(0.001%) vs 株式配当(3~5%)。その差は数千倍。"; Category = "戦略" },
    @{No = 66; Title = "今日が一番若い"; Content = "始めるなら今がベストタイミング。"; Category = "戦略" },
    @{No = 67; Title = "長期 vs 短期"; Content = "目先の利益より、将来の大きな果実。"; Category = "戦略" },
    @{No = 68; Title = "失敗と学び"; Content = "失敗から何を学ぶかが重要。"; Category = "戦略" },
    @{No = 69; Title = "投資仲間"; Content = "孤独にならない。情報共有し、励まし合う。"; Category = "戦略" },
    @{No = 70; Title = "嫉妬 vs 祝福"; Content = "他人の成功を喜べるか。付き合う人で人生が変わる。"; Category = "戦略" },
    @{No = 71; Title = "自己投資"; Content = "最もリターンの高い投資は自分自身への投資。"; Category = "戦略" },
    @{No = 72; Title = "バランス"; Content = "金、健康、人間関係。どれか一つ欠けても不幸。"; Category = "戦略" },
    @{No = 73; Title = "権利確定日"; Content = "この日に株を持っていないと配当や優待はもらえない。"; Category = "戦略" },
    @{No = 74; Title = "株主優待"; Content = "日本独自の文化。商品やサービス券がもらえる。"; Category = "戦略" },
    @{No = 75; Title = "ジャーナリング"; Content = "書く瞑想。思考を紙に書き出して整理する。"; Category = "戦略" },
    @{No = 76; Title = "リテラシー"; Content = "日本は金融リテラシーが低い。勉強しないと搾取される。"; Category = "未来" },
    @{No = 77; Title = "海外の教育"; Content = "海外では子供の頃からお金の授業がある。"; Category = "未来" },
    @{No = 78; Title = "感情のコントロール"; Content = "興奮や恐怖で売買しない。機械的になる。"; Category = "未来" },
    @{No = 79; Title = "ストップ高/安"; Content = "日本株の値幅制限。行き過ぎた動きを止める仕組み。"; Category = "未来" },
    @{No = 80; Title = "管理(再)"; Content = "スプレッドシート等で資産を可視化し続ける。"; Category = "未来" },
    @{No = 82; Title = "毎月配当(再)"; Content = "インカムゲインの積み上げこそがFIREへの道。"; Category = "未来" },
    @{No = 83; Title = "ETF(再)"; Content = "個別株より低リスク。初心者の最適解。"; Category = "未来" },
    @{No = 84; Title = "Grokで銘柄探し"; Content = "AIを活用して有望銘柄を見つける。"; Category = "未来" },
    @{No = 85; Title = "ChatGPT壁打ち"; Content = "投資判断の相談相手としてAIを使う。"; Category = "未来" },
    @{No = 86; Title = "お金と平穏"; Content = "枕を高くして眠れる投資をする。"; Category = "未来" },
    @{No = 87; Title = "カルダシェフ尺度"; Content = "文明の進化レベル。人類はまだタイプ0。進化は続く。"; Category = "未来" },
    @{No = 88; Title = "脳内チップ"; Content = "ニューラリンク。人間とAIの融合。"; Category = "未来" },
    @{No = 89; Title = "宇宙太陽光"; Content = "無限のエネルギー。新しい産業。"; Category = "未来" },
    @{No = 90; Title = "連想ゲーム"; Content = "「風が吹けば桶屋が儲かる」。ニュースから関連銘柄を探す。"; Category = "未来" },
    @{No = 91; Title = "ピケティ(再)"; Content = "富の集中は加速する。投資側に回るしかない。"; Category = "未来" },
    @{No = 92; Title = "孫子の兵法"; Content = "「負けないこと」が大事。生き残ればチャンスは来る。"; Category = "未来" },
    @{No = 93; Title = "100年単位"; Content = "人生100年時代。超長期視点で考える。"; Category = "未来" },
    @{No = 94; Title = "致命傷を避ける"; Content = "再起不能な損失（退場）だけは避ける。"; Category = "未来" },
    @{No = 95; Title = "虎穴に入らずんば"; Content = "リスクを取らなければリターン（虎子）は得られない。バランス。"; Category = "未来" },
    @{No = 96; Title = "長期のメリット"; Content = "複利効果、ストレス減、税金繰り延べ効果。"; Category = "未来" },
    @{No = 97; Title = "デイトレ"; Content = "専業（ガチ勢）の世界。修羅の道。"; Category = "未来" },
    @{No = 98; Title = "平均取得単価"; Content = "ナンピン買いで単価を下げる技術。"; Category = "未来" },
    @{No = 99; Title = "損切り(再)"; Content = "サンクコストバイアスを捨てる。"; Category = "未来" },
    @{No = 100; Title = "戻る暴落"; Content = "世界経済は右肩上がり。信じて待つ。"; Category = "未来" },
    @{No = 101; Title = "確率論"; Content = "10回引けば当たるなら、試行回数を増やす。分散投資。"; Category = "未来" }
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "レミの兵法投資 - 101フォルダ一括生成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$successCount = 0
$errorCount = 0

foreach ($tip in $tips) {
    try {
        # フォルダ名を作成（例: No01_配当貴族）
        $folderName = "No{0:D3}_{1}" -f $tip.No, $tip.Title
        $folderPath = Join-Path $baseDir $folderName
        
        # フォルダ作成
        if (-not (Test-Path $folderPath)) {
            New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
        }
        
        # プロンプトファイルのパス
        $promptFile = Join-Path $folderPath "プロンプト.md"
        
        # プロンプト内容を生成
        $promptContent = @"
# No.$($tip.No)「$($tip.Title)」2P漫画生成プロンプト

## 📋 TIP情報

| 項目 | 内容 |
|------|------|
| **No** | $($tip.No) |
| **タイトル** | $($tip.Title) |
| **解説** | $($tip.Content) |
| **カテゴリー** | $($tip.Category) |

---

## 🎨 1ページ目プロンプト

``````
【⚠️ CRITICAL LAYOUT INSTRUCTION】
MANGA PAGE 1 - VERTICAL DYNAMIC PANEL LAYOUT
- Panel 1 (TOP 40%): Large horizontal panel
- Panel 2 (MIDDLE 30%): Medium horizontal panel  
- Panel 3 (BOTTOM-LEFT 15%): Small vertical panel
- Panel 4 (BOTTOM-RIGHT 15%): Small vertical panel
ALL PANELS ARRANGED VERTICALLY IN READING ORDER FROM TOP TO BOTTOM.
Portrait aspect ratio (9:16).

【⚠️ TEXT BOX REQUIREMENT】
In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:
「テーマ：$($tip.Title)」
Font: Bold, Clear Japanese Gothic font.

【🎨 スタイル仕様】
- Japanese manga style
- 6500K neutral white balance
- Clean bright colors with cel shading
- White panel borders with black outlines
- Pure white speech bubbles
- Professional manga quality

【✨ 演出効果】
- Sparkle effects (キラキラ)
- Light particles (光の粒子)
- Motion lines where appropriate

Title: $($tip.Title)

【Panel 1】導入 (Large top panel - 40%)
Scene: Modern elegant office room with large windows showing city skyline. Afternoon sunlight streaming in.
Characters: 
- Yuto (優斗): (Traditional Japanese black GAKURAN school uniform:1.5), (High stiff stand-up collar:1.4), (Gold buttons:1.3), short black hair, curious expression
- Remi (レミ): (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Sharp almond-shaped eyes:1.2), wearing (tailored RED blazer:1.3) over black lace top, confident smile
Composition: Yuto on left, Remi on right
Dialogue:
- 優斗: 「姉さん、『$($tip.Title)』について教えてください！」
TEXT BOX (bottom-right corner): 「テーマ：$($tip.Title)」 in black box with white border

---

【Panel 2】展開 (Medium panel - 30%)
Scene: Close-up of Remi explaining with confident expression
Characters: Remi in focus
Dialogue:
- レミ: 「良い質問ね。$($tip.Content)」

---

【Panel 3】反応 (Small left panel - 15%)
Scene: Yuto's surprised or thoughtful reaction
Characters: Yuto's face close-up
Effects: Appropriate reaction effects
Dialogue:
- 優斗: 「なるほど！」

---

【Panel 4】予告 (Small right panel - 15%)
Scene: Remi with confident expression
Characters: Remi's profile
Effects: Sparkle effects
Dialogue:
- レミ: 「詳しく説明するわね」
``````

---

## 🎨 2ページ目プロンプト

``````
【⚠️ CRITICAL LAYOUT INSTRUCTION】
MANGA PAGE 2 - DYNAMIC MIXED PANEL LAYOUT
- Panel 1 (TOP 50%): Large wide horizontal cinematic panel
- Panel 2 (MIDDLE-LEFT 25%): Vertical panel on left side
- Panel 3 (MIDDLE-RIGHT 25%): Vertical panel on right side
- Panel 4 (BOTTOM 25%): Wide horizontal conclusion panel
ALL PANELS flow naturally for vertical reading.
Portrait aspect ratio (9:16).

【🎨 スタイル仕様】
- Japanese manga style with dramatic cinematic shots
- 6500K neutral white balance
- Rich colors with dynamic contrast
- White panel borders with black outlines
- Pure white speech bubbles

【✨ 演出効果】
- Visual metaphors related to the topic
- Dynamic effects and backgrounds
- Professional manga quality

Title: $($tip.Title)

【Panel 1】ビジュアル解説 (Large cinematic top panel - 50%)
Scene: Dramatic visual representation of the concept
Effects: Cinematic and impactful
Narration box (top-left): 「$($tip.Content)」

---

【Panel 2】ポイント① (Left vertical panel - 25%)
Scene: Visual metaphor for key point 1
Narration box: 「ポイント①を視覚化」

---

【Panel 3】ポイント② (Right vertical panel - 25%)  
Scene: Visual metaphor for key point 2
Narration box: 「ポイント②を視覚化」

---

【Panel 4】オチ・完結 (Wide bottom panel - 25%)
Scene: Back in the office. Both characters looking satisfied
Characters:
- Yuto (left): (GAKURAN uniform:1.4), inspired expression
- Remi (right): (Silver hair:1.5), (Red eyes:1.4), (Red blazer:1.3), proud smile
Composition: Two-shot with positive atmosphere
Effects: Warm light particles
Dialogue:
- 優斗: 「わかりました！実践してみます！」
- レミ: 「その意気よ。着実に進めていきなさい」
``````

---

## 📝 メモ欄

このプロンプトは基本テンプレートです。
実際に画像生成する際は、以下をカスタマイズしてください：

1. **具体的なシーン設定**
2. **キャラクターの表情と動作**
3. **セリフの詳細化**
4. **ビジュアルメタファーの選定**
5. **カテゴリー（$($tip.Category)）に応じた演出**

---

**作成日**: 2026-02-03  
**ステータス**: ⚠️ 要カスタマイズ  
**次のステップ**: プロンプトを詳細化してから画像生成
"@

        # ファイルに書き込み
        $promptContent | Out-File -FilePath $promptFile -Encoding UTF8
        
        Write-Host "[OK] No.$($tip.No.ToString().PadLeft(3)) - $($tip.Title)" -ForegroundColor Green
        $successCount++
        
    }
    catch {
        Write-Host "[ERROR] No.$($tip.No) - $($tip.Title): $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "完了サマリー" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "成功: $successCount フォルダ" -ForegroundColor Green
Write-Host "失敗: $errorCount フォルダ" -ForegroundColor Red
Write-Host "合計: $($tips.Count) フォルダ" -ForegroundColor Cyan
Write-Host ""
Write-Host "フォルダ作成場所: $baseDir" -ForegroundColor Yellow
Write-Host ""
