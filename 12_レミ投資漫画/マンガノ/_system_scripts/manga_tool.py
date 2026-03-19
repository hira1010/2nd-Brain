# -*- coding: utf-8 -*-
"""
Manga Production CLI Tool
統合管理ツール。以下の機能をこれ一本で実行可能にします。
- generate: プロンプト/Markdownの生成
- fix: プロンプトの修正（文字置換など）
- themes: キーワード/テーマの更新
- email: 完成データのメール送信
"""
import argparse
import sys
import os
import re
import datetime
import smtplib
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

# 共通設定・ユーティリティのインポート
try:
    import manga_config as config
    import manga_utils as utils
except ImportError:
    # 同一ディレクトリにない場合を見越してパスを通す（基本は同一ディレクトリ想定）
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import manga_config as config
    import manga_utils as utils

# コンソールエンコーディング設定
utils.setup_console_encoding()


# =================================================================================
# 1. Generate Logic
# =================================================================================
def _build_pages_content(ep: Dict[str, object]) -> str:
    start_page, end_page = utils.parse_page_range(str(ep["range"]))
    pages: List[str] = []
    for page in range(start_page, end_page + 1):
        pages.append(
            config.PROMPT_TEMPLATE.format(
                p=page,
                version=config.PROMPT_VERSION,
                version_upper=config.PROMPT_VERSION.upper(),
                ep_no=ep["no"],
                desc=ep["desc"],
                title=ep["title"],
            )
        )
    return "".join(pages)


def _build_markdown_content(ep: Dict[str, object], pages_content: str) -> str:
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    return f"""# No102 Episode {ep['no']}: {ep['title']} ({ep['range']})

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| EP | {ep['no']} |
| タイトル | {ep['title']} |
| 解説 | {ep['desc']} |

---

{pages_content}

作成日: {today_str}
ステータス: {ep['range']} {config.PROMPT_VERSION} 完了
"""


def command_generate(args):
    print(">>> Running Generation...")
    utils.ensure_directory(config.BASE_DIR)

    count = 0
    for ep in config.EPISODES:
        filepath = utils.get_episode_filename(ep, config.BASE_DIR)
        
        # もし --force がなく、ファイルが存在する場合はスキップするか確認してもよいが、
        # 既存ツールは上書き動作だったので上書きする
        pages_content = _build_pages_content(ep)
        content = _build_markdown_content(ep, pages_content)
        
        if args.dry_run:
            print(f"[DryRun] Would generate: {os.path.basename(filepath)}")
        else:
            if utils.save_text_file(filepath, content):
                count += 1
    
    print(f"Generation completed. {count} files processed.")


# =================================================================================
# 2. Fix Prompts Logic
# =================================================================================
_EXCLUDED_FILE = "00_ストーリー構成.md"
_ARCH_PATTERN = re.compile(r"ARCHITECTURE: \[v15\.5 EDGE OBLITERATOR\].*?12:17\.")

def _apply_replacements(content: str, new_arch_line: str) -> str:
    updated = content
    updated = updated.replace(
        "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS.",
        config.CHAR_YUTO,
    )
    updated = updated.replace("- Yuto: (BLACK Gakuran).", "- Yuto: (NAVY BUSINESS SUIT).")
    updated = updated.replace("{Yuto: (BLACK Gakuran)}", "{Yuto: (NAVY BUSINESS SUIT)}")
    updated = _ARCH_PATTERN.sub(new_arch_line, updated)
    updated = updated.replace("Gakuran", "Business Suit")
    return updated


def command_fix(args):
    print(">>> Running Prompt Fixer...")
    target_dir = config.STORY_DIR
    if not os.path.exists(target_dir):
        print(f"Target directory not found: {target_dir}")
        return

    new_arch_line = config.HEADER_TEMPLATE.split("\n", 1)[0]
    
    count = 0
    for filename in os.listdir(target_dir):
        if not filename.endswith(".md") or filename == _EXCLUDED_FILE:
            continue
            
        filepath = os.path.join(target_dir, filename)
        content = utils.load_text_file(filepath)
        if content is None:
            continue

        fixed_content = _apply_replacements(content, new_arch_line)

        if content != fixed_content:
            if args.dry_run:
                print(f"[DryRun] Would fix: {filename}")
            else:
                if utils.save_text_file(filepath, fixed_content):
                    print(f"Fixed: {filename}")
                    count += 1
    
    print(f"Fix completed. {count} files updated.")


# =================================================================================
# 3. Update Themes Logic
# =================================================================================
def _get_updated_keywords():
    return {
        "EP04.5_未来年表.md": {
            "theme": "未来年表",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **未来年表** | 「人生にかかるお金を年表にしてみよう。見えないものは怖い。でも見えれば、対策が打てる」 |
| 人生コスト＝約2億円 | 「住宅・教育・老後…普通に生きるだけで2億円必要。給料だけで足りると思う？」 |
| 給与所得の限界 | 「年収500万でも手取りは400万以下。ここから2億円を捻り出すのは…そう、無理ゲーだ」 |"""
        },
        "EP06.5_72の法則.md": {
            "theme": "複利",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **複利** | 「利息に利息がつく。これが複利の魔法。アインシュタインが"人類最大の発明"と呼んだ力だ」 |
| 72の法則 | 「72÷利回り＝資産が倍になる年数。年利7%なら約10年で倍。覚えておけ、この公式」 |
| 単利 vs 複利 | 「単利は足し算、複利は掛け算。時間が経つほど、この差は雪だるま式に広がる」 |"""
        },
        "EP08.5_時間の武器.md": {
            "theme": "ドルコスト平均法",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **ドルコスト平均法** | 「毎月同じ金額を買い続ける。高い時は少なく、安い時は多く買える。感情を排除する最強の仕組みだ」 |
| 定額積立 | 「月3万円でいい。大事なのは金額じゃない。"止めないこと"だ」 |
| 暴落＝バーゲンセール | 「株が50%下がった？ それは同じお金で2倍買えるってことだ。泣くな、喜べ」 |"""
        },
        "EP10.5_逆張りの思考.md": {
            "theme": "逆張り",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **逆張り** | 「みんなが恐怖で逃げる時に買い、みんなが熱狂で群がる時に売る。これが投資家の真髄だ」 |
| 大衆心理の逆を行く | 「SNSが"終わりだ"と叫ぶ時こそ、歴史的な買い場。バフェットの名言を思い出せ」 |
| 恐怖と歓喜 | 「"他人が恐怖で売る時に買い、他人が歓喜で買う時に売れ"——ウォーレン・バフェット」 |"""
        },
        "EP12.5_最強の投資家.md": {
            "theme": "長期投資",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **長期投資** | 「最も運用成績が良かった"属性"は——すでに亡くなった人だった。なぜか？ 何もしなかったからだ」 |
| 何もしない勇気 | 「売りたくなる。不安になる。でも最強の投資家は"何もしない"ことを選んだ人だ」 |
| 忍耐＝最大のリターン | 「20年間S&P500を持ち続けた人で、損をした人は歴史上ゼロ。時間が最大の味方だ」 |"""
        },
        "EP15.5_黄金の果樹園.md": {
            "theme": "分散投資",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **分散投資** | 「1本の木に頼るな。500本の果樹園を持て。1本が枯れても、残りの499本が果実を実らせる」 |
| S&P500＝果樹園 | 「S&P500は米国トップ500社の詰め合わせ。これ1つで世界最強の分散投資が完成する」 |
| 配当再投資 | 「果実（配当）を食べるな。土に植え直せ。すると果樹園はどんどん広がっていく」 |"""
        },
        "EP20.5_自由の定義.md": {
            "theme": "FIRE",
            "keywords_table": """| キーワード | レミの解説 |
| :--- | :--- |
| **FIRE** | 「Financial Independence, Retire Early——経済的独立と早期引退。でも本当の意味は"働かない"じゃない」 |
| 4%ルール | 「年間生活費の25倍の資産があれば、毎年4%ずつ使っても資産は減らない。これが自由の方程式だ」 |
| 労働は"義務"から"選択"へ | 「FIREの本質は"仕事を辞める"ことじゃない。"好きな仕事を選べる自由"を手に入れることだ」 |"""
        }
    }

EP17_5_NEW = """# Episode 17.5: 配当貴族 (P85.5)

## TIP情報

| 項目 | 内容 |
| :--- | :--- |
| EP | 17.5 |
| タイトル | 配当貴族 |
| 解説 | 25年以上連続増配を続ける「配当貴族」銘柄の存在。不景気でも配当を増やし続ける企業の強さと、配当金が生む"第2の給料"の仕組み。 |

---

## 🔑 キーワード枠（レミの解説時に画面表示）

| キーワード | レミの解説 |
| :--- | :--- |
| **配当貴族** | 「25年以上、毎年配当金を増やし続けている企業がある。リーマンショックでもコロナでも。これが"貴族"と呼ばれる理由だ」 |
| 配当金＝第2の給料 | 「株を持っているだけで、毎年お金が振り込まれる。寝ていても、旅行中でも。これが配当金だ」 |
| 増配の複利効果 | 「最初は年間1万円の配当でも、増配＋再投資を20年続ければ…年間50万円以上になる可能性がある」 |

---

## 📈 優斗の成長（Lv.7 収入の柱を増やす）

優斗の投資口座に、初めてまとまった配当金が入金される。レミは「これが"配当貴族"の力だ。コカ・コーラ、P&G、ジョンソン＆ジョンソン…25年以上連続で配当を増やし続けている企業がある。これらに分散投資すれば、君の"第2の給料"が毎年勝手に増えていく」と教える。優斗は「働かなくてもお金が入ってくる」という概念を初めて実体験し、投資の本質を理解する。

---

## 📉 田中の対比（退職・一家離散）

一方の田中は、全てを一発逆転に賭け続けた結果、ついに限界を迎える。家賃を滞納し、妻から三行半を突きつけられ、退職。「コツコツ配当を受け取る」という地味だが確実な道を選ばず、「一発で大金を稼ぐ」というギャンブル思考にすがり続けた代償が、人生の崩壊という形で現れる。優斗が"配当という第2の給料"を手に入れた同じ瞬間、田中は本業の給料すら失った。

---

## 85.5-A ページ目 (v15.5 Edge Obliterator - Refined)

```javascript
generate_image(
  ImageName: "remi_ep17_5_a_final_v1",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**

CHARACTERS:
- Remi: (PINK WAVY HAIR, EMERALD GREEN EYES). (WHITE BLOUSE + EMERALD RIBBON). (Confident, teacher-like expression, pointing to a chart). **VISUAL LOCK**.
- Yuto: (NAVY BUSINESS SUIT). (Amazed expression, looking at his phone). **VISUAL LOCK**.

[PANEL 1 - 45% height]: FULL WIDTH FILL. [Medium Shot] Remi stands before a golden chart showing company logos (Coca-Cola, P&G, J&J silhouettes) wearing golden crowns. Above them, the text '配当貴族 - 25年連続増配'. A red carpet rolls out from these logos. Yuto watches in amazement.
STRICT SPEECH BUBBLE WITH JAPANESE TEXT: 'リーマンショックでもコロナでも、配当を増やし続けた企業がある。これが"貴族"だ'

[PANEL 2 - 30% height]: FULL WIDTH FILL. [Close-up] Yuto's smartphone showing a notification: '配当金入金: ¥15,000'. His face lights up with wonder. Keywords float in decorative golden frames: '配当貴族' '第2の給料' '増配の複利効果'
STRICT SPEECH BUBBLE WITH JAPANESE TEXT: 'え…寝てただけなのに、お金が入ってきた…！'

[PANEL 3 - 25% height]: FULL WIDTH FILL. [Split Panel] LEFT: Yuto smiling, golden coins gently raining from small tree icons (dividend trees growing). RIGHT: Dark silhouette of Tanaka at a desk, head in hands, a termination letter in front of him. The contrast - one gains a second income, the other loses his only income.

STYLE: [PREMIUM DIGITAL MANGA]. High-end 2D Anime, Crisp linework, Vibrant colors, Dynamic cinematic lighting, Sharp Cel Shading, Masterpiece quality. OBLITERATE ALL CANVAS MARGINS. ALL PANELS MUST BLEED TO ABSOLUTE EDGE. ZERO WHITE SPACE.
**NEGATIVE PROMPT**: metadata at top, ImageName at top, filename at top, 12:17 at top, title at top, gibberish text, hallucinated letters, technical labels, architecture text, panel labels, white margins, white borders."
)
```

---

## 85.5-B ページ目 (v15.5 Edge Obliterator - Refined)

```javascript
generate_image(
  ImageName: "remi_ep17_5_b_final_v1",
  Prompt: "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. **VERTICAL PORTRAIT ORIENTATION. 12:17 RATIO.**

CHARACTERS:
- Remi: (PINK WAVY HAIR, EMERALD GREEN EYES). (WHITE BLOUSE + EMERALD RIBBON). (Warm, encouraging smile). **VISUAL LOCK**.
- Yuto: (NAVY BUSINESS SUIT). (Confident, determined expression). **VISUAL LOCK**.

[PANEL 1 - 50% height]: FULL WIDTH FILL. [Dramatic Infographic Style] A beautiful timeline visualization. Year 1: small tree with tiny golden fruit (¥10,000/year). Year 10: medium tree with more fruit (¥100,000/year). Year 20: massive golden tree overflowing with fruit (¥500,000+/year). The caption reads '増配 × 再投資 × 時間 ＝ 配当貴族の真価'.
STRICT SPEECH BUBBLE WITH JAPANESE TEXT: '最初は小さな果実でも、増配と再投資を続ければ…20年後には"第2の給料"になる'

[PANEL 2 - 25% height]: FULL WIDTH FILL. [Medium Shot] Remi holding up two paths visually - LEFT PATH (golden, bright): labeled '毎月コツコツ配当', showing Yuto walking calmly on a golden road. RIGHT PATH (dark, crumbling): labeled '一発逆転ギャンブル', showing Tanaka's silhouette falling into darkness.
STRICT SPEECH BUBBLE WITH JAPANESE TEXT: '一発逆転を狙う者は全てを失い、コツコツ積み上げる者が貴族になる'

[PANEL 3 - 25% height]: FULL WIDTH FILL. [Close-up] Yuto writing in his investment notebook. The page shows: '配当貴族に学ぶこと: ①25年の忍耐 ②増配の力 ③再投資の掛け算'. His eyes show determination and growth.

STYLE: [PREMIUM DIGITAL MANGA]. High-end 2D Anime, Crisp linework, Vibrant colors, Dynamic cinematic lighting, Sharp Cel Shading, Masterpiece quality. OBLITERATE ALL CANVAS MARGINS. ALL PANELS MUST BLEED TO ABSOLUTE EDGE. ZERO WHITE SPACE.
**NEGATIVE PROMPT**: metadata at top, ImageName at top, filename at top, 12:17 at top, title at top, gibberish text, hallucinated letters, technical labels, architecture text, panel labels, white margins, white borders."
)
```

---

作成日: 2026-02-11
ステータス: EP17.5 (配当貴族) Created
"""

def _update_keyword_section(filepath: str, new_table: str) -> bool:
    content = utils.load_text_file(filepath)
    if not content:
        return False

    lines = content.split('\n')
    result = []
    in_keyword_section = False
    in_keyword_table = False
    table_replaced = False

    for line in lines:
        if 'キーワード枠' in line and '##' in line:
            in_keyword_section = True
            result.append(line)
            continue

        if in_keyword_section and not table_replaced:
            if line.strip().startswith('|') and 'キーワード' in line:
                in_keyword_table = True
                result.append(new_table)
                continue
            elif in_keyword_table:
                if line.strip().startswith('|'):
                    continue
                else:
                    in_keyword_table = False
                    table_replaced = True
                    in_keyword_section = False
                    result.append(line)
                    continue
            else:
                result.append(line)
                continue
        else:
            result.append(line)

    new_content = '\n'.join(result)
    utils.save_text_file(filepath, new_content)
    return True


def command_themes(args):
    print(">>> Running Theme/Keywords Updater...")
    updated_keywords = _get_updated_keywords()
    
    # 1. Update existing ep files
    for filename, data in updated_keywords.items():
        filepath = os.path.join(config.STORY_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping (not found): {filename}")
            continue
            
        if args.dry_run:
             print(f"[DryRun] Would update keywords in: {filename}")
        else:
            if _update_keyword_section(filepath, data["keywords_table"]):
                print(f"Updated: {filename} -> Theme: {data['theme']}")

    if args.dry_run:
        print("[DryRun] Skipping file creation/deletion (EP17.5)")
        return

    # 2. EP17.5 Replacement
    old_path = os.path.join(config.STORY_DIR, "EP17.5_生活防衛資金.md")
    new_path = os.path.join(config.STORY_DIR, "EP17.5_配当貴族.md")

    if os.path.exists(old_path):
        os.remove(old_path)
        print(f"Deleted: EP17.5_生活防衛資金.md")

    utils.save_text_file(new_path, EP17_5_NEW.strip() + '\n')
    print(f"Created: EP17.5_配当貴族.md")
    
    # 3. List update
    list_path = os.path.join(config.STORY_DIR, '00_新規生成リスト_ここからスタート.md')
    if os.path.exists(list_path):
        content = utils.load_text_file(list_path)
        if content:
            content = content.replace('生活防衛資金', '配当貴族')
            content = content.replace('生活費6ヶ月分の確保と安全地帯の構築', '配当貴族銘柄と第2の給料の仕組み')
            utils.save_text_file(list_path, content)
            print("Updated: 00_新規生成リスト_ここからスタート.md")


# =================================================================================
# 4. Email Logic
# =================================================================================
class MangaEmailSender:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.sender = config.EMAIL_SENDER
        self.password = config.EMAIL_PASSWORD
        self.receiver = config.EMAIL_RECEIVER

    def collect_files(self):
        # 簡易実装: config.STORY_DIR から最新のMDファイルを拾う、あるいは
        # 生成された "No102_..." スタイルのファイルを探す
        # ここでは config.BASE_DIR (作成済みフォルダ的な場所) を探査対象とする
        files = []
        if os.path.exists(config.BASE_DIR):
            for f in os.listdir(config.BASE_DIR):
                if f.startswith("No102_") and f.endswith(".md"):
                    files.append(Path(os.path.join(config.BASE_DIR, f)))
        return sorted(files, key=lambda x: x.name)

    def create_message(self, files):
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg["Subject"] = config.EMAIL_SUBJECT
        msg.attach(MIMEText(config.EMAIL_BODY, "plain"))

        for filepath in files:
            self._attach_file(msg, filepath)
        return msg

    def _attach_file(self, msg, filepath):
        filename = filepath.name
        with open(filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(part)

    def run(self):
        files = self.collect_files()
        if not files:
            print("No files found to send.")
            return

        print(f"Found {len(files)} files to send.")
        if self.dry_run:
            print("[DryRun] Skipping email send.")
            for f in files:
                print(f" - {f.name}")
            return

        msg = self.create_message(files)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


def command_email(args):
    print(">>> Running Email Sender...")
    sender = MangaEmailSender(dry_run=args.dry_run)
    sender.run()


# =================================================================================
# Main Entry Point
# =================================================================================
def main():
    parser = argparse.ArgumentParser(description="Manga Production CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate
    parser_gen = subparsers.add_parser("gen", help="Generate manga prompts/markdowns")
    parser_gen.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser_gen.set_defaults(func=command_generate)

    # Fix
    parser_fix = subparsers.add_parser("fix", help="Fix prompt text in story files")
    parser_fix.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser_fix.set_defaults(func=command_fix)

    # Themes
    parser_themes = subparsers.add_parser("themes", help="Update theme keywords and create EP17.5")
    parser_themes.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser_themes.set_defaults(func=command_themes)

    # Email
    parser_email = subparsers.add_parser("email", help="Send generated files via email")
    parser_email.add_argument("--dry-run", action="store_true", help="Simulate email sending")
    parser_email.set_defaults(func=command_email)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
