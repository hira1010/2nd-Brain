import pyautogui
import time
import sys

print("--- Kindle撮影範囲 座標取得ツール ---")
print("マウスカーソルの現在の座標をリアルタイムで表示します。")
print("")
print("1. Kindle Cloud Reader（ブラウザ）を画面に表示してください。")
print("2. 本文エリアの「左上端（カド）」にマウスを合わせ、表示される X, Y をメモ。")
print("3. 次に「右下端（カド）」にマウスを合わせ、表示される X, Y をメモ。")
print("4. メモした値を kindle_ocr.py の CAPTURE_REGION に設定してください。")
print("")
print("中断するには Ctrl+C を押してください。")
print("-" * 30)

try:
    while True:
        x, y = pyautogui.position()
        position_str = f"現在の位置 -> X: {x:>4} Y: {y:>4}"
        sys.stdout.write(f"\r{position_str}")
        sys.stdout.flush()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n座標の取得を終了しました。")
