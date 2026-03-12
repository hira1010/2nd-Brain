"""
danbooru_prompt_fetcher.py
Danbooru API からタグ（プロンプト）を取得して ComfyUI に渡すスクリプト。
"""

import json
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# プロジェクトルートをパスに追加
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.append(str(_root))

# ComfyUI コントローラーをインポート（起動中の場合のみ使用）
try:
    from comfyui_controller import is_running, queue_prompt
    COMFYUI_AVAILABLE = True
except ImportError:
    COMFYUI_AVAILABLE = False

# ====================================================================
# 定数
# ====================================================================

DANBOORU_API = "https://danbooru.donmai.us/posts.json"

# MetaタグはComfyUIプロンプトには不要なので除外
EXCLUDE_META_TAGS = {
    "highres", "absurdres", "commentary", "commentary_request",
    "english_commentary", "translated", "translation_request",
    "paid_reward_available", "third-party_edit",
}

# レート制限（Danbooru の利用規約に従い 1秒に1リクエスト以内）
REQUEST_INTERVAL = 1.2  # 秒


# ====================================================================
# Danbooru API
# ====================================================================

def fetch_posts(
    page: int = 1,
    limit: int = 20,
    tags: str = "",
    rating: str = "g",
) -> List[Dict[str, Any]]:
    """
    Danbooru から投稿を取得する。

    Args:
        page:   ページ番号（1始まり）
        limit:  1ページあたりの取得数（最大200）
        tags:   検索タグ（スペース区切り、例: "1girl red_hair"）
        rating: レーティング絞り込み "g"=全年齢, "s"=センシティブ, "q"=questionable, "e"=explicit, ""=すべて

    Returns:
        投稿データのリスト
    """
    params: Dict[str, Any] = {
        "page": page,
        "limit": min(limit, 200),
    }

    # タグ検索条件を組み立て
    search_tags = tags.split() if tags else []
    if rating:
        search_tags.append(f"rating:{rating}")
    if search_tags:
        params["tags"] = " ".join(search_tags)

    print(f"🔍 Danbooru取得中: page={page}, limit={limit}, tags={params.get('tags', '(なし)')}")
    response = requests.get(DANBOORU_API, params=params, timeout=15)
    response.raise_for_status()
    posts = response.json()
    print(f"✅ {len(posts)} 件取得")
    return posts


def extract_prompt(post: Dict[str, Any], include_artist: bool = False) -> str:
    """
    投稿データから ComfyUI 用プロンプト文字列を生成する。

    Args:
        post:           Danbooru の投稿データ
        include_artist: アーティストタグを含めるか

    Returns:
        カンマ区切りのプロンプト文字列
    """
    tags: List[str] = []

    # 一般タグ（メインのビジュアル説明）
    general = post.get("tag_string_general", "")
    for tag in general.split():
        if tag not in EXCLUDE_META_TAGS:
            tags.append(tag.replace("_", " "))

    # キャラクタータグ
    for tag in post.get("tag_string_character", "").split():
        tags.append(tag.replace("_", " "))

    # アーティストタグ（オプション）
    if include_artist:
        for tag in post.get("tag_string_artist", "").split():
            tags.append(f"by {tag.replace('_', ' ')}")

    return ", ".join(tags)


def fetch_prompts(
    pages: int = 1,
    limit_per_page: int = 20,
    tags: str = "",
    rating: str = "g",
    include_artist: bool = False,
    shuffle: bool = True,
) -> List[str]:
    """
    複数ページにわたってプロンプトを収集する。

    Args:
        pages:           取得するページ数
        limit_per_page:  1ページあたりの件数
        tags:            絞り込みタグ
        rating:          レーティング
        include_artist:  アーティストタグ含むか
        shuffle:         結果をシャッフルするか

    Returns:
        プロンプト文字列のリスト
    """
    all_prompts: List[str] = []

    for page in range(1, pages + 1):
        posts = fetch_posts(page=page, limit=limit_per_page, tags=tags, rating=rating)
        for post in posts:
            prompt = extract_prompt(post, include_artist=include_artist)
            if prompt:
                all_prompts.append(prompt)
        if page < pages:
            time.sleep(REQUEST_INTERVAL)

    if shuffle:
        random.shuffle(all_prompts)

    print(f"📝 合計 {len(all_prompts)} 件のプロンプトを取得")
    return all_prompts


def save_prompts(prompts: List[str], output_path: Path) -> None:
    """プロンプト一覧を JSON ファイルに保存する。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    print(f"💾 保存: {output_path} ({len(prompts)} 件)")


def load_prompts(path: Path) -> List[str]:
    """保存済みプロンプトを読み込む。"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ====================================================================
# ComfyUI 連携
# ====================================================================

def build_workflow_with_prompt(
    positive_prompt: str,
    negative_prompt: str = "lowres, bad anatomy, bad hands, text, error, blurry",
    checkpoint: str = "illustriousXL_v01.safetensors",
    width: int = 1024,
    height: int = 1024,
    steps: int = 20,
    cfg: float = 7.0,
    sampler: str = "euler",
) -> Dict[str, Any]:
    """
    指定プロンプトで ComfyUI API ワークフローを生成する。

    Returns:
        ComfyUI API 形式のワークフロー辞書
    """
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
                "seed": random.randint(0, 2**32 - 1),
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": "normal",
                "denoise": 1.0,
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": checkpoint},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["4", 1], "text": positive_prompt},
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["4", 1], "text": negative_prompt},
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"images": ["8", 0], "filename_prefix": "danbooru"},
        },
    }


def run_batch(
    prompts: List[str],
    count: int = 5,
    checkpoint: str = "illustriousXL_v01.safetensors",
    interval: float = 2.0,
) -> None:
    """
    プロンプトリストから ComfyUI にバッチ生成キューを送る。

    Args:
        prompts:    プロンプトのリスト
        count:      生成する枚数
        checkpoint: 使用するモデル名
        interval:   キュー間の待機秒数
    """
    if not COMFYUI_AVAILABLE:
        print("❌ comfyui_controller がインポートできません")
        return
    if not is_running():
        print("❌ ComfyUI が起動していません。先に起動してください。")
        return

    selected = prompts[:count] if len(prompts) >= count else prompts
    print(f"🚀 {len(selected)} 件をキューに追加します...")

    for i, prompt in enumerate(selected, 1):
        print(f"\n[{i}/{len(selected)}] プロンプト: {prompt[:80]}...")
        workflow = build_workflow_with_prompt(prompt, checkpoint=checkpoint)
        queue_prompt(workflow)
        if i < len(selected):
            time.sleep(interval)

    print("\n✅ すべてキューに追加しました！")


# ====================================================================
# CLI
# ====================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Danbooru からプロンプトを取得して ComfyUI に送る"
    )
    parser.add_argument("--tags",    default="1girl",         help='絞り込みタグ（例: "1girl red_hair"）')
    parser.add_argument("--rating",  default="g",             help='レーティング: g/s/q/e/（空=すべて）')
    parser.add_argument("--pages",   type=int, default=1,     help="取得ページ数")
    parser.add_argument("--limit",   type=int, default=20,    help="1ページあたりの件数")
    parser.add_argument("--save",    metavar="FILE",          help="プロンプトを JSON ファイルに保存")
    parser.add_argument("--load",    metavar="FILE",          help="保存済み JSON からプロンプトを読み込む")
    parser.add_argument("--run",     type=int, metavar="N",   help="N 件を ComfyUI に送って生成")
    parser.add_argument("--model",   default="illustriousXL_v01.safetensors", help="使用するモデル名")
    parser.add_argument("--artist",  action="store_true",     help="アーティストタグも含める")
    parser.add_argument("--show",    type=int, metavar="N",   help="N 件プロンプトを表示")
    args = parser.parse_args()

    # プロンプト取得
    if args.load:
        prompts = load_prompts(Path(args.load))
        print(f"📂 {len(prompts)} 件読み込み: {args.load}")
    else:
        prompts = fetch_prompts(
            pages=args.pages,
            limit_per_page=args.limit,
            tags=args.tags,
            rating=args.rating,
            include_artist=args.artist,
        )

    # 保存
    if args.save:
        save_prompts(prompts, Path(args.save))

    # 表示
    if args.show:
        for i, p in enumerate(prompts[: args.show], 1):
            print(f"\n[{i}] {p}")

    # ComfyUI 実行
    if args.run:
        run_batch(prompts, count=args.run, checkpoint=args.model)

    # 何もオプションがなければ最初の5件を表示
    if not any([args.save, args.load, args.run, args.show]):
        print("\n--- 取得プロンプト (先頭5件) ---")
        for i, p in enumerate(prompts[:5], 1):
            print(f"[{i}] {p[:100]}...")
