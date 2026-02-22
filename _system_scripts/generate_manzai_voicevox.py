
import os
import re
import requests
import json
import argparse
import time
from pathlib import Path
import sys

# ==========================================
# 設定エリア (Voicevox)
# ==========================================
VOICEVOX_URL = "http://127.0.0.1:50021"

# キャラクターID設定 (VoicevoxのIDを指定)
# ※ 一般的なID (環境によって異なる場合があります)
# 2: 四国めたん (ノーマル) -> レミ
# 3: ずんだもん (ノーマル) -> 優斗 (仮: 男性ボイスが良い場合は変更推奨)
# 11: 玄野武宏 (ノーマル) -> 男性ボイス
# 13: 剣崎雌雄 (ノーマル) -> 男性ボイス

SPEAKER_MAPPING = {
    "レミ": 2,      # 四国めたん (ノーマル)
    "優斗": 13,     # 剣崎雌雄 (ノーマル) - 若い男性
    "二人": 13      # 仮
}

# ==========================================

def check_voicevox_status():
    try:
        response = requests.get(f"{VOICEVOX_URL}/version", timeout=3)
        if response.status_code == 200:
            print(f"Voicevox 接続成功: バージョン {response.json()}")
            return True
    except requests.exceptions.ConnectionError:
        print("エラー: Voicevox が起動していません。")
        print("Voicevoxアプリを起動し、ローカルサーバー(ポート50021)が有効になっているか確認してください。")
        return False
    return False

def parse_script(file_path):
    """Markdown台本からセリフを抽出する"""
    dialogues = []
    if not os.path.exists(file_path):
        print(f"エラー: 元ファイルが見つかりません: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"\|\s*[\d:]+\s*\|\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\s*\|", line)
            if match:
                speaker = match.group(1).strip()
                content = match.group(2).strip()
                text_match = re.search(r"「(.*?)」", content)
                text = text_match.group(1) if text_match else content.replace("「", "").replace("」", "")
                text = re.sub(r"<.*?>", "", text)
                dialogues.append({"speaker": speaker, "text": text})
    return dialogues

def generate_voicevox_audio(index, speaker, text, output_dir):
    speaker_id = SPEAKER_MAPPING.get(speaker)
    
    # マッピングにない場合はデフォルト(レミ=2)または警告
    if speaker_id is None:
        print(f"警告: 話者 '{speaker}' のIDが未定義です。デフォルト(2:四国めたん)を使用します。")
        speaker_id = 2

    print(f"生成中 ({index:02d}): {speaker}(ID:{speaker_id}) 「{text[:10]}...」")

    # 1. Audio Query
    try:
        query_payload = {"text": text, "speaker": speaker_id}
        query_res = requests.post(f"{VOICEVOX_URL}/audio_query", params=query_payload)
        
        if query_res.status_code != 200:
            print(f"   -> Queryエラー: {query_res.text}")
            return

        query_data = query_res.json()

        # 2. Synthesis
        synth_payload = {"speaker": speaker_id}
        # query_dataはJSON bodyとして送る
        synth_res = requests.post(f"{VOICEVOX_URL}/synthesis", params=synth_payload, json=query_data)

        if synth_res.status_code == 200:
            filename = f"{index:02d}_{speaker}_{text[:5]}.wav"
            filename = re.sub(r'[\\/*?:"<>|]', "", filename)
            output_path = output_dir / filename
            
            with open(output_path, "wb") as f:
                f.write(synth_res.content)
            print(f"   -> 保存完了: {output_path}")
        else:
            print(f"   -> Synthesisエラー: {synth_res.text}")

    except Exception as e:
        print(f"   -> 例外発生: {e}")

def main():
    parser = argparse.ArgumentParser(description="Markdown台本からVoicevoxで漫談音声を生成します。")
    parser.add_argument("script_file", help="入力するMarkdown台本ファイルのパス")
    parser.add_argument("--output", "-o", default="audio_voicevox", help="出力先ディレクトリ")
    
    args = parser.parse_args()
    
    if not check_voicevox_status():
        return

    script_file = Path(args.script_file)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Voicevox 漫談音声自動生成スタート ===")
    dialogues = parse_script(script_file)
    
    if not dialogues:
        print("セリフが見つかりませんでした。")
        return

    print(f"合計 {len(dialogues)} 行のセリフを検出しました。")
    print("-" * 30)

    for i, d in enumerate(dialogues, 1):
        generate_voicevox_audio(i, d["speaker"], d["text"], output_dir)
        time.sleep(0.1) # 負荷軽減

    print("-" * 30)
    print(f"完了しました。出力先: {output_dir}")

if __name__ == "__main__":
    main()
