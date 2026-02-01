import pyautogui
import pygetwindow as gw
import time
import os
from PIL import Image
import pytesseract
from datetime import datetime

# ==========================================
# 設定セクション (ユーザー設定)
# ==========================================
# Tesseractのインストールパス (Windowsの場合は必須)
# 例: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 保存先設定
OUTPUT_DIR = r'c:\Users\hirak\Desktop\2nd-Brain\03_Kindle\Kindle解析'
BOOK_TITLE = "緑内障"  # 解析する本の名前
MAX_PAGES = 1000        # 撮影・解析するページ数（自動停止するので多めでOK）

# 撮影範囲（Kindle Cloud Readerの本文エリア座標）
# (左上のX, 左上のY, 幅, 高さ)
CAPTURE_REGION = (52, 182, 1695, 764) 

# ウェイト設定 (秒)
PAGE_WAIT = 2.5  # ページめくり後の待機時間（長めにして精度UP）

# ==========================================
# メイン処理
# ==========================================



if __name__ == "__main__":
    # ユーザーに入力を求める
    print("\n" + "="*40)
    print("   Kindle OCR Tool 設定")
    print("="*40)
    
    title_input = input(f"1. 本のタイトルを入力 (デフォルト: {BOOK_TITLE}): ")
    if title_input.strip():
        BOOK_TITLE = title_input.strip()

    try:
        pages_input = input(f"2. 全ページ数を入力 (デフォルト: {MAX_PAGES}): ")
        if pages_input.strip():
            MAX_PAGES = int(pages_input)
    except ValueError:
        print(f"   ! 無効な入力。{MAX_PAGES} ページで続行します。")

    direction_input = input("3. ページを送る方向を入力 (L: 左 / R: 右) [デフォルト L]: ").upper()
    PAGE_DIRECTION = 'right' if direction_input == 'R' else 'left'

    print("\n" + "-"*40)
    print(f"📖 設定完了: 「{BOOK_TITLE}」")
    print(f"📑 ページ数: {MAX_PAGES}")
    print(f"➡️ 送り方向: {PAGE_DIRECTION}")
    print("-"*40)
    
    print("\n【超重要：手順】")
    print("1. このターミナルを画面の「端」に移動して、Kindleを隠さないようにする。")
    print("2. ブラウザのKindle画面を開き、表紙を表示する。")
    print("3. エンターキーを押すと 5秒カウントダウン が始まります。")
    input("\n準備ができたらエンターキーを押してください...")

    # 実行前に5秒待機
    for i in range(5, 0, -1):
        print(f"⏳ {i}秒後に開始します... Kindle画面を最前面にしてください！")
        time.sleep(1)
    
    # ページめくり方向を引数に渡すように関数を微調整するか、グローバルを参照させる
    def capture_and_ocr_with_config(direction):
        # 保存フォルダの作成
        # 日付をなくしてタイトルのみのフォルダにする
        save_path = os.path.join(OUTPUT_DIR, BOOK_TITLE)
        os.makedirs(save_path, exist_ok=True)
        
        md_file_path = os.path.join(save_path, f"{BOOK_TITLE}.md")
        
        print(f"\n🚀 実行中...")
        
        # 重複検知用の前ページ画像データ
        last_screenshot_bytes = None
        
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(f"# {BOOK_TITLE} 解析ログ\n\n")
            f.write(f"取得日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")

            # 最初に画面中央をクリックしてフォーカスを当てる
            center_x = CAPTURE_REGION[0] + CAPTURE_REGION[2] // 2
            center_y = CAPTURE_REGION[1] + CAPTURE_REGION[3] // 2
            pyautogui.click(center_x, center_y)
            time.sleep(1)

            # ページ数を自動判定するために上限を増やしておく
            actual_page_count = 0
            
            for page in range(0, MAX_PAGES):
                current_label = "Cover" if page == 0 else f"Page {page}"
                print(f"📄 {current_label} (処理中...)")
                
                # 1. キャプチャ
                screenshot = pyautogui.screenshot(region=CAPTURE_REGION)
                
                # 重複チェック（ページがめくれていない＝終了とみなす）
                current_bytes = screenshot.tobytes()
                if last_screenshot_bytes and current_bytes == last_screenshot_bytes:
                    print(f"🛑 ページが変化しないため終了します (Total: {actual_page_count} pages)")
                    break
                
                last_screenshot_bytes = current_bytes
                actual_page_count += 1
                
                # 2. OCR
                if page == 0:
                    text_h = pytesseract.image_to_string(screenshot, lang='jpn')
                    text_v = pytesseract.image_to_string(screenshot, lang='jpn_vert')
                    text = f"--- Cover OCR (Horizontal) ---\n{text_h}\n\n--- Cover OCR (Vertical) ---\n{text_v}"
                else:
                    text = pytesseract.image_to_string(screenshot, lang='jpn_vert')
                
                # 3. 保存
                f.write(f"## {current_label}\n\n")
                f.write(text)
                f.write("\n\n---\n\n")
                
                # 4. めくる
                pyautogui.press(direction)
                time.sleep(PAGE_WAIT)

        print(f"\n✅ 全ページの処理が完了しました！")
        print(f"結果保存先: {save_path}")

    capture_and_ocr_with_config(PAGE_DIRECTION)

def clean_ocr_text(text):
    """OCRテキストのノイズ除去と整形"""
    # 既知のゴミ文字列を削除
    garbage_patterns = [
        "エエ で ぎ 「[C マ ンマ スロ トー マー ロス mu ニス ズ ロ Cu「 で カベ て て mumm ロ ニニ で マー",
        "ケロ スラ コロ ュ ョ る マミ",
        "911OG悦直り",
        "Q\n", "S\n"
    ]
    for p in garbage_patterns:
        text = text.replace(p, "")
    
    # 0L -> OL などの修正
    text = text.replace("0L", "OL")
    
    return text.strip()

def sanitize_filename(name):
    """ファイル名に使えない文字を置換"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()[:50] # 長すぎるとエラーになるので詰める

def preprocess_image(image):
    """OCR精度向上のための画像前処理"""
    # グレースケール変換
    gray = image.convert('L')
    # 二値化 (閾値は128あたりが一般的だが、Kindleの文字は見やすいので少し調整)
    # 薄い文字を飛ばさないよう、閾値を調整するか、単純なグレースケールでも十分な場合が多い
    # ここではコントラストを上げる簡易的な処理
    return gray

if __name__ == "__main__":
    # ユーザーに入力を求める
    print("\n" + "="*40)
    print("   Kindle OCR Tool (Auto Mode)")
    print("="*40)
    
    # タイトル入力
    print(f"1. 本のタイトル (Enterで表紙OCRから自動取得): ")
    title_input = input("   > ").strip()
    
    AUTO_TITLE = False
    if not title_input:
        BOOK_TITLE = "Unknown_Title_" + datetime.now().strftime('%Y%m%d_%H%M%S')
        AUTO_TITLE = True
        print("   👉 表紙OCRから自動決定します")
    else:
        BOOK_TITLE = title_input
        AUTO_TITLE = False

    # ページ数入力 (実質無限)
    MAX_PAGES = 3000
    print(f"2. ページ数: 自動判別モードで実行します (最大 {MAX_PAGES} ページ)")
    print("   (ページがめくれなくなったら自動停止します)")

    direction_input = input("3. ページ送り方向 (L: 左 / R: 右) [Enter=L]: ").upper()
    PAGE_DIRECTION = 'right' if direction_input == 'R' else 'left'

    print("\n" + "-"*40)
    print(f"📖 タイトル: {BOOK_TITLE} (Auto: {AUTO_TITLE})")
    print(f"➡️ 送り方向: {PAGE_DIRECTION}")
    print("-"*40)
    
    print("\n【手順】")
    print("1. この画面を端に寄せる。")
    print("2. Kindleで表紙を表示する。")
    print("3. Enterを押すと開始。")
    input("\nReady? Press Enter...")

    for i in range(3, 0, -1):
        print(f"⏳ {i}...")
        time.sleep(1)
    
    # 保存フォルダの初期化 (タイトル確定前は仮フォルダを使用せず、メモリ内で保持してから書き込む手もあるが、
    # 途中経過保存のために一旦仮フォルダを使うか、表紙OCRだけ先に行う)
    
    output_base = OUTPUT_DIR
    
    # 重複検知用
    last_screenshot_bytes = None
    actual_page_count = 0
    
    # MDファイルハンドルはタイトル確定後に開く
    # そのため、まず表紙を処理する
    
    print(f"\n📸 表紙をスキャン中...")
    
    # 表紙キャプチャ
    cover_shot = pyautogui.screenshot(region=CAPTURE_REGION)
    processed_cover = preprocess_image(cover_shot)
    
    cover_text_h = pytesseract.image_to_string(processed_cover, lang='jpn')
    cover_text_v = pytesseract.image_to_string(processed_cover, lang='jpn_vert')
    
    # タイトル自動決定ロジック
    if AUTO_TITLE:
        # 横書きテキストの最初の空白でない行を採用
        candidates = [line.strip() for line in cover_text_h.split('\n') if line.strip()]
        if candidates:
            detected_title = candidates[0]
            # 短すぎる場合は2行目も見るかも？一旦シンプルに
            BOOK_TITLE = sanitize_filename(detected_title)
            print(f"💡 タイトルを検出しました: {BOOK_TITLE}")
        else:
            print("⚠️ タイトル検出失敗。タイムスタンプ名を使用します。")
    
    # フォルダ作成
    save_path = os.path.join(output_base, BOOK_TITLE)
    os.makedirs(save_path, exist_ok=True)
    md_file_path = os.path.join(save_path, f"{BOOK_TITLE}.md")
    
    print(f"📂 保存先: {save_path}")
    print(f"🚀 解析開始...")

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(f"# {BOOK_TITLE} 解析ログ\n\n")
        f.write(f"取得日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        
        # 表紙書き込み
        f.write("## Cover\n\n")
        f.write(f"--- Cover OCR (Horizontal) ---\n{clean_ocr_text(cover_text_h)}\n\n")
        f.write(f"--- Cover OCR (Vertical) ---\n{clean_ocr_text(cover_text_v)}\n\n")
        f.write("---\n\n")
        
        # 1ページ目へ
        pyautogui.press(PAGE_DIRECTION)
        time.sleep(PAGE_WAIT)
        
        last_screenshot_bytes = cover_shot.tobytes()
        actual_page_count = 1
        
        # 本文ループ
        for page in range(1, MAX_PAGES):
            print(f"📄 Page {page}...", end='\r')
            
            screenshot = pyautogui.screenshot(region=CAPTURE_REGION)
            
            # 重複判定
            current_bytes = screenshot.tobytes()
            # 完全一致だとたまにずれるので、少し許容するか？
            # いや、スクリーンショットなのでデジタルデータなら完全一致するはず
            if current_bytes == last_screenshot_bytes:
                print(f"\n🛑 ページ末尾に到達しました。(Total: {actual_page_count} pages)")
                break
            
            last_screenshot_bytes = current_bytes
            actual_page_count += 1
            
            # 前処理とOCR
            processed_img = preprocess_image(screenshot)
            text = pytesseract.image_to_string(processed_img, lang='jpn_vert')
            cleaned_text = clean_ocr_text(text)
            
            f.write(f"## Page {page}\n\n")
            f.write(cleaned_text)
            f.write("\n\n---\n\n")
            
            # めくる
            pyautogui.press(PAGE_DIRECTION)
            time.sleep(PAGE_WAIT)

    print(f"\n✅ 完了！ {md_file_path}")
