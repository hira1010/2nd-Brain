import os
import re
import requests
import json
from pathlib import Path

# ==========================================
# 設定エリア
# ==========================================
# Eleven Labs APIキー（環境変数から取得、またはここに直接記入）
# ※セキュリティのため、環境変数 'ELEVEN_LABS_API_KEY' の使用を推奨します。
API_KEY = os.environ.get("ELEVEN_LABS_API_KEY") or ""

# ボイスID設定（Eleven LabsのVoice LabからIDを取得して書き換えてください）
# ここでは初期値として一般的なボイスIDを設定しています。
VOICE_ID_REMI = "21m00Tcm4TlvDq8ikWAM"  # 例: Rachel (女性)
VOICE_ID_YUTO = "TxGEqnHWrfWFTfGW9XjX"  # 例: Josh (男性)

# ファイル設定
SCRIPT_FILE = Path("Manzai_Script_60sec.md")
OUTPUT_DIR = Path("audio")

# ==========================================

def parse_script(file_path):
    """Markdown台本からセリフを抽出する"""
    dialogues = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Markdownテーブル行の解析
            # パターン: | 時間 | **話者** | 「セリフ」 | ...
            match = re.search(r"\|\s*[\d:]+\s*\|\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\s*\|", line)
            if match:
                speaker = match.group(1).strip()
                content = match.group(2).strip()
                
                # 「」の中身だけ抽出（もしあれば）
                text_match = re.search(r"「(.*?)」", content)
                text = text_match.group(1) if text_match else content.replace("「", "").replace("」", "")
                
                # SSMLタグの除去（簡易的）
                text = re.sub(r"<.*?>", "", text)
                
                dialogues.append({"speaker": speaker, "text": text})
    return dialogues

def generate_audio(index, speaker, text):
    """Eleven Labs APIを叩いて音声を保存する"""
    if not API_KEY:
        print(f"[シミュレーション] {index:02d}_{speaker}: {text}")
        print("   -> APIキーが設定されていないため、音声生成をスキップしました。")
        return

    # 話者に応じたボイスID選択
    if "レミ" in speaker:
        voice_id = VOICE_ID_REMI
        stability = 0.50
    elif "優斗" in speaker:
        voice_id = VOICE_ID_YUTO
        stability = 0.40
    else:
        print(f"警告: 未知の話者 '{speaker}' です。スキップします。")
        return

    print(f"生成中 ({index:02d}): {speaker}「{text[:10]}...」")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            filename = f"{index:02d}_{speaker}_{text[:5]}.mp3"
            #ファイル名に使えない文字を除去
            filename = re.sub(r'[\\/*?:"<>|]', "", filename)
            output_path = OUTPUT_DIR / filename
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"   -> 保存完了: {output_path}")
        else:
            print(f"   -> エラー: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   -> 例外発生: {e}")

def main():
    if not SCRIPT_FILE.exists():
        print(f"エラー: 台本ファイル '{SCRIPT_FILE}' が見つかりません。")
        return

    # 出力ディレクトリ作成
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=== 漫談音声自動生成スタート ===")
    dialogues = parse_script(SCRIPT_FILE)
    
    if not dialogues:
        print("セリフが見つかりませんでした。Markdownの形式を確認してください。")
        return

    print(f"合計 {len(dialogues)} 行のセリフを検出しました。")
    print("-" * 30)

    for i, d in enumerate(dialogues, 1):
        generate_audio(i, d["speaker"], d["text"])

    print("-" * 30)
    if not API_KEY:
        print("※ APIキーを設定すると、実際に音声ファイル(mp3)が生成されます。")
        print("  設定方法: スクリプト内の 'API_KEY' 変数にキーを貼るか、環境変数に設定してください。")
    else:
        print("すべての処理が完了しました。 'audio' フォルダを確認してください。")

if __name__ == "__main__":
    main()
