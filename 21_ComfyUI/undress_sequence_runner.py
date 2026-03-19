"""
undress_sequence_runner.py
段階的に服を脱いでいくシークエンスを ComfyUI で生成するスクリプト。
"""

import json
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# プロジェクトルートをパスに追加
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.append(str(_root))

try:
    from comfyui_controller import queue_prompt, is_running, upload_image
    COMFYUI_AVAILABLE = True
except ImportError:
    COMFYUI_AVAILABLE = False

# ====================================================================
# 設定
# ====================================================================

# 基本設定（脱衣シークエンス）
SEQUENCE = [
    {"label": "01_full_angry", "clothing": "wearing full clothes, black business suit, white shirt", "expression": "angry, looking at viewer"},
    {"label": "02_shirt_shy", "clothing": "wearing only white shirt, (jacket removed:1.3)", "expression": "shy, slightly blushing"},
    {"label": "03_underwear_emb", "clothing": "wearing bra and black panties, (shirt removed:1.4)", "expression": "blushing, embarrassed"},
    {"label": "04_naked_hands", "clothing": "(nude:1.6), (bra removed:1.4), covering breasts with hands", "expression": "extremely embarrassed, heavy blushing, looking away"},
]

DEFAULT_CHECKPOINT = "dreamshaper_8.safetensors"

# ====================================================================
# ワークフロー構築 (Inpainting版)
# ====================================================================

def build_inpainting_workflow(
    positive_prompt: str,
    negative_prompt: str,
    image_filename: str,
    seed: int,
    checkpoint: str = DEFAULT_CHECKPOINT,
) -> Dict[str, Any]:
    """ControlNetでポーズを固定しつつ、インペイントで脱がせるワークフロー。"""
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint}
        },
        "2": {
            "class_type": "LoadImage",
            "inputs": {"image": image_filename, "upload": "image"}
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["1", 1], "text": positive_prompt}
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["1", 1], "text": negative_prompt}
        },
        "5": {
            "class_type": "APersonMaskGenerator",
            "inputs": {
                "images": ["2", 0],
                "face_mask": True,
                "background_mask": False,
                "hair_mask": False,
                "body_mask": True,
                "clothes_mask": True,
                "confidence": 0.4,
                "refine_mask": True
            }
        },
        "6": {
            "class_type": "ControlNetLoader",
            "inputs": {"control_net_name": "control_v11f1p_sd15_depth_fp16.safetensors"}
        },
        "7": {
            "class_type": "ControlNetApply",
            "inputs": {
                "conditioning": ["3", 0],
                "control_net": ["6", 0],
                "image": ["2", 0],
                "strength": 0.8
            }
        },
        "8": {
            "class_type": "VAEEncodeForInpaint",
            "inputs": {
                "pixels": ["2", 0],
                "vae": ["1", 2],
                "mask": ["5", 0],
                "grow_mask_by": 12
            }
        },
        "9": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["7", 0],
                "negative": ["4", 0],
                "latent_image": ["8", 0],
                "seed": seed,
                "steps": 25,
                "cfg": 8.0,
                "sampler_name": "euler_ancestral",
                "scheduler": "karras",
                "denoise": 0.75
            }
        },
        "10": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["9", 0], "vae": ["1", 2]}
        },
        "11": {
            "class_type": "SaveImage",
            "inputs": {"images": ["10", 0], "filename_prefix": "undress_seq"}
        }
    }

# ====================================================================
# 実行
# ====================================================================

def run_sequence(image_path: str, seed: Optional[int] = None, model: str = DEFAULT_CHECKPOINT) -> None:
    if not COMFYUI_AVAILABLE:
        print("❌ comfyui_controller.py が不足しています。")
        return
    
    if not is_running():
        print("❌ ComfyUI が起動していません。")
        return

    img_path = Path(image_path)
    if not img_path.exists():
        print(f"❌ 元画像が見つかりません: {image_path}")
        return

    # 画像のアップロード
    print(f"📤 画像をアップロード中: {img_path.name}")
    upload_res = upload_image(img_path)
    image_name = upload_res["name"]

    if seed is None:
        seed = random.randint(0, 2**32 - 1)
    
    # 共通のネガティブプロンプト (HUD消去のため text box を追加)
    negative_base = "lowres, bad anatomy, bad hands, text, error, blurry, (text box, HUD, watermark, floating limbs:1.5)"

    print(f"🚀 脱衣シークエンス開始 (Seed: {seed})")

    for step in SEQUENCE:
        label = step["label"]
        clothing = step["clothing"]
        expression = step["expression"]
        
        # インペイント用のポジティブプロンプト
        pos = f"1girl, (detailed face:1.2), {clothing}, {expression}, masterpiece, best quality"
        # 脱衣のときは服のネガティブをさらに強める
        neg = f"{negative_base}, (clothes, shirt, suit, tie, jacket, bra, panties:1.4)" if "naked" in label or "underwear" in label else negative_base
        
        print(f"  - ステップ: {label}")
        workflow = build_inpainting_workflow(pos, neg, image_name, seed, checkpoint=model)
        
        try:
            queue_prompt(workflow)
        except Exception as e:
            print(f"  ❌ 失敗: {e}")
        
        time.sleep(1.0)

    print("\n✅ 生成リクエスト完了。ComfyUIで確認してください。")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="元絵（リファレンス画像）のパス")
    parser.add_argument("--seed", type=int, help="固定シード値")
    parser.add_argument("--model", default=DEFAULT_CHECKPOINT, help="使用するモデル名")
    args = parser.parse_args()

    run_sequence(image_path=args.image, seed=args.seed, model=args.model)
