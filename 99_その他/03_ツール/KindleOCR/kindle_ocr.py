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
