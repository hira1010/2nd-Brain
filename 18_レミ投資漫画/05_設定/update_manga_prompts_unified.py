#!/usr/bin/env python3
"""
漫画プロンプト統合更新スクリプト
全7つの更新スクリプトを統合し、モード選択で実行可能にしたバージョン
"""

import argparse
import os
import re
import manga_config as config
import manga_utils as utils
from manga_prompt_builder import MangaPromptBuilder


def load_template(path):
    """テンプレートファイルを読み込む"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_visual_instruction(title, description):
    """タイトルと説明から視覚的指示を生成"""
    return f"Draw a conceptual illustration representing '{description}'."


# ========== モード: FULL - 完全な再生成（テンプレート適用）==========
def mode_full(filepath, dry_run=False):
    """完全な再生成モード (apply_gemini_template.py ベース)"""
    TEMPLATE_1P_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\00_漫画生成テンプレート_1P.md"
    TEMPLATE_2P_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\00_漫画生成テンプレート_2P.md"
    
    TEMPLATE_1P = load_template(TEMPLATE_1P_PATH)
    TEMPLATE_2P = load_template(TEMPLATE_2P_PATH)
    
    content = utils.read_file(filepath)
    meta = utils.parse_metadata(content)
    
    if 'number' not in meta:
        print(f"  SKIP: No number found in {os.path.basename(filepath)}")
        return False
    
    # ページ数決定
    page_count = int(meta.get('page_count', 2))
    
    # テンプレート選択
    template = TEMPLATE_1P if page_count == 1 else TEMPLATE_2P
    
    # 変数準備
    number = meta.get('number', '00')
    title = meta.get('title', 'Untitled')
    description = meta.get('description', 'No description')
    category = meta.get('category', 'Uncategorized')
    
    # セリフ
    d_theme = f"優斗君、今日は『{title}』について教えるわよ。"
    d_teach_1 = meta.get('dialogue_teach', f"いい心がけね。でも、ただ知るだけじゃ意味がないわ。 つまり、{description}")
    d_action_1 = "なるほど…！ イメージできました！"
    
    d_summary = f"{description} これが投資の本質よ。しっかり頭に叩き込みなさい。"
    d_action_2 = f"そうか…{title}の本質はここにあったんですね。"
    
    # 視覚的指示
    visual_1 = generate_visual_instruction(title, description)
    visual_2 = "(Use symbolic imagery to represent the concept)"
    
    # 置換
    new_content = template.replace("{NUMBER}", str(number))
    new_content = new_content.replace("{TITLE}", title)
    new_content = new_content.replace("{DESCRIPTION}", description)
    new_content = new_content.replace("{CATEGORY}", category)
    new_content = new_content.replace("{DIALOGUE_THEME}", d_theme)
    new_content = new_content.replace("{DIALOGUE_TEACH_1}", d_teach_1)
    new_content = new_content.replace("{DIALOGUE_ACTION_1}", d_action_1)
    
    if page_count > 1:
        new_content = new_content.replace("{DIALOGUE_SUMMARY}", d_summary)
        new_content = new_content.replace("{DIALOGUE_ACTION_2}", d_action_2)
        new_content = new_content.replace("{VISUAL_INSTRUCTION_2}", visual_2)
    
    new_content = new_content.replace("{VISUAL_INSTRUCTION_1}", visual_1)
    
    if not dry_run:
        utils.write_file(filepath, new_content)
    return True


# ========== モード: SLIM - スリム化のみ ==========
def mode_slim(filepath, dry_run=False):
    """スリム化モード (apply_slim_prompts.py ベース)"""
    content = utils.read_file(filepath)
    original = content
    
    # 1. サイズと比率 (1200x1697)
    content = content.replace("1200x1700", "1200x1697")
    content = content.replace("1700 pixels height", "1697 pixels height")
    content = content.replace("aspect ratio 12:17", "aspect ratio 1200:1697")
    content = content.replace("Aspect Ratio: 12:17", "Aspect Ratio: 1200:1697")
    content = content.replace("ratio (9:16)", "ratio (1200:1697)")
    
    # 2. キャラクター定義の最新化
    old_remi_patterns = [
        "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent. BARE HANDS (no gloves).",
        "Remi (Woman): Silky SILVER hair, Red eyes, Red blazer.",
        "Remi: Silky SILVER hair, Red eyes, Red blazer.",
        "(Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)",
        "Remi: (Silky SILVER hair:1.5), (Vibrant RED eyes:1.4), (Tailored RED blazer:1.3)."
    ]
    for p in old_remi_patterns:
        content = content.replace(p, config.REMI_DEF)
    
    old_yuto_patterns = [
        "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner. BARE HANDS (no gloves).",
        "Yuto (Boy): Short Black hair, Black GAKURAN uniform.",
        "Yuto: Short Black hair, Black GAKURAN uniform.",
        "Short Black hair, (Traditional Black GAKURAN school uniform:1.4)",
        "Yuto: Short Black hair, (Traditional Black GAKURAN school uniform:1.4)."
    ]
    for p in old_yuto_patterns:
        content = content.replace(p, config.YUTO_DEF)
    
    # 3. 描画ミス誘発テキストの削除
    content = re.sub(r'画像生成を行ってください。.*?\n', '', content)
    content = re.sub(r'\[OUTPUT: .*?\]\n', '', content)
    
    if config.PREFIX not in content:
        content = content.replace("```text", f"```text\n{config.PREFIX}\n")
    
    # 4. セクション見出しの普通の言葉化
    content = content.replace("MANDATORY IMAGE SPECIFICATIONS:", "Technical Setup:")
    content = content.replace("CRITICAL ANATOMICAL REQUIREMENTS:", "Character Anatomy:")
    content = content.replace("PANEL LAYOUT - PAGE 1:", "Page 1 Layout:")
    content = content.replace("PANEL LAYOUT - PAGE 2:", "Page 2 Layout:")
    content = content.replace("STYLE SPECIFICATIONS:", "Art Style:")
    content = content.replace("TEXT BOX REQUIREMENT:", "Title Box Design:")
    
    # 5. タイトルボックス配置修正
    old_box = "In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:"
    content = content.replace(old_box, config.NEW_TITLE_BOX_INSTRUCTION)
    
    changed = content != original
    if changed and not dry_run:
        utils.write_file(filepath, content)
    return changed


# ========== モード: VARIATION - バリエーション適用 ==========
def mode_variation(filepath, dry_run=False):
    """バリエーション適用モード (apply_variations.py ベース)"""
    content = utils.read_file(filepath)
    
    # メタデータ解析
    meta = utils.parse_metadata(content)
    if 'number' not in meta:
        print(f"  SKIP: No metadata in {os.path.basename(filepath)}")
        return False
    
    # ビルダーでコンテンツ生成
    builder = MangaPromptBuilder(meta)
    new_p1_content = builder.build_page1()
    new_p2_content = builder.build_page2()
    page_count = builder.page_count
    
    new_full_content = content
    
    # 1ページ目ヘッダー決定
    p1_header = "## 1ページ目プロンプト" if page_count > 1 else "## プロンプト"
    
    # P1ブロック置換
    p1_pattern = r'## (1ページ目プロンプト|プロンプト)\s*\n\s*```text\s*\n(.*?)\n```'
    p1_replacement = f"{p1_header}\n\n```text\n{new_p1_content}\n```"
    
    if re.search(p1_pattern, new_full_content, flags=re.DOTALL):
        new_full_content = re.sub(p1_pattern, p1_replacement, new_full_content, flags=re.DOTALL)
    
    # P2ブロック置換
    p2_pattern = r'## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
    
    if page_count > 1 and new_p2_content:
        p2_replacement = f"## 2ページ目プロンプト\n\n```text\n{new_p2_content}\n```"
        if re.search(p2_pattern, new_full_content, flags=re.DOTALL):
            new_full_content = re.sub(p2_pattern, p2_replacement, new_full_content, flags=re.DOTALL)
    else:
        # ページ1: P2を削除
        new_full_content = re.sub(p2_pattern, "", new_full_content, flags=re.DOTALL)
        new_full_content = re.sub(r'\n\s*\n\s*\n', '\n\n', new_full_content)
    
    changed = new_full_content != content
    if changed and not dry_run:
        utils.write_file(filepath, new_full_content)
    return changed


# ========== モード: SAFE - 安全な更新のみ ==========
def mode_safe(filepath, dry_run=False):
    """安全な更新モード (apply_variations_safe.py + update_prompts_bulk.py ベース)"""
    content = utils.read_file(filepath)
    original_content = content
    
    # メタデータ解析
    meta = utils.parse_metadata(content)
    if 'number' not in meta:
        return False
    
    # 1. 解剖学的要件の追加
    if "Character Anatomy:" not in content and "CRITICAL ANATOMICAL REQUIREMENTS" not in content:
        target = "Resolution: High quality manga illustration"
        content = content.replace(target, f"{target}\n\n{config.ANATOMY_BLOCK}")
    
    # 2. キャラクター定義の更新 (BARE HANDS追加)
    remi_old = "Remi (Woman): Silky SILVER hair, Vibrant RED eyes, Red blazer, Black lace top, Cool & Intelligent."
    if remi_old in content and "BARE HANDS" not in content[content.find(remi_old):content.find(remi_old)+200]:
        content = content.replace(remi_old, config.REMI_DEF)
    
    yuto_old = "Yuto (Boy): Short Black hair, Black GAKURAN school uniform, Energetic & Learner."
    if yuto_old in content and "BARE HANDS" not in content[content.find(yuto_old):content.find(yuto_old)+200]:
        content = content.replace(yuto_old, config.YUTO_DEF)
    
    # 3. 命令プレフィックスの追加
    def add_prefix(match):
        block_content = match.group(1)
        if config.PREFIX not in block_content and "【IMAGE_GENERATION_TASK】" not in block_content:
            return f"```text\n{config.PREFIX}\n{block_content}```"
        return match.group(0)
    
    content = re.sub(r"```text\n(.*?)```", add_prefix, content, flags=re.DOTALL)
    
    changed = content != original_content
    if changed and not dry_run:
        utils.write_file(filepath, content)
    return changed


# ========== メイン処理 ==========
def main():
    parser = argparse.ArgumentParser(description='漫画プロンプト統合更新スクリプト')
    parser.add_argument('--mode', 
                        choices=['full', 'slim', 'variation', 'safe'],
                        default='variation',
                        help='更新モード: full=完全再生成, slim=スリム化, variation=バリエーション, safe=安全更新')
    parser.add_argument('--dry-run', action='store_true', help='テスト実行（ファイル変更なし）')
    parser.add_argument('--skip', nargs='*', default=[], help='スキップするファイル番号（例: 26 28）')
    
    args = parser.parse_args()
    
    # モード選択
    mode_functions = {
        'full': mode_full,
        'slim': mode_slim,
        'variation': mode_variation,
        'safe': mode_safe
    }
    
    mode_func = mode_functions[args.mode]
    mode_name = {
        'full': '完全再生成',
        'slim': 'スリム化',
        'variation': 'バリエーション適用',
        'safe': '安全更新'
    }[args.mode]
    
    print("=" * 70)
    print(f"漫画プロンプト統合更新スクリプト - モード: {mode_name}")
    if args.dry_run:
        print("🔍 ドライラン・モード (ファイルは変更されません)")
    print("=" * 70)
    print()
    
    count = 0
    total = 0
    
    for filepath in utils.find_manga_prompt_files(config.BASE_DIR):
        total += 1
        filename = os.path.basename(filepath)
        
        # スキップ処理
        skip_numbers = [f"No{n}_" for n in args.skip]
        if any(skip_num in filename for skip_num in skip_numbers):
            print(f"⊘ SKIP (指定): {filename}")
            continue
        
        print(f"[{total}] Processing: {filename}... ", end='')
        
        try:
            if mode_func(filepath, dry_run=args.dry_run):
                print("✓ DONE" if not args.dry_run else "✓ WOULD UPDATE")
                count += 1
            else:
                print("⊘ NO CHANGE")
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    print()
    print("=" * 70)
    action = "更新" if not args.dry_run else "更新予定"
    print(f"完了: {count}/{total} ファイルを{action}")
    print("=" * 70)


if __name__ == "__main__":
    main()
