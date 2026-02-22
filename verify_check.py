from pathlib import Path
from typing import Dict, List

SOURCE_DIR = Path(
    r"c:/Users/hirak/Desktop/2nd-Brain/18_繝ｬ繝滓兜雉・ｼｫ逕ｻ/繝槭Φ繧ｬ繝・01_髟ｷ邱ｨ_蟶梧悍縺ｮ謚戊ｳ・01_繧ｹ繝医・繝ｪ繝ｼ"
)
OUTPUT_FILE = Path(r"c:/Users/hirak/Desktop/2nd-Brain/verify_result.txt")
EPISODE_MARKER = ".5_"

THEMES = [
    "譛ｪ譚･蟷ｴ陦ｨ",
    "隍・茜",
    "繝峨Ν繧ｳ繧ｹ繝亥ｹｳ蝮・ｳ・,",
    "騾・ｼｵ繧・,",
    "髟ｷ譛滓兜雉・,",
    "蛻・淵謚戊ｳ・,",
    "驟榊ｽ楢ｲｴ譌・,",
    "FIRE",
]

KEYWORDS: Dict[str, str] = {
    "KW": "繧ｭ繝ｼ繝ｯ繝ｼ繝画棧",
    "YT": "蜆ｪ譁励・謌宣聞",
    "TN": "逕ｰ荳ｭ縺ｮ蟇ｾ豈・",
    "RM": "繝ｬ繝溘・隗｣隱ｬ",
}


def list_episode_files(directory: Path) -> List[Path]:
    return sorted(
        [path for path in directory.iterdir() if path.is_file() and path.suffix == ".md" and EPISODE_MARKER in path.name]
    )


def check_markers(content: str) -> Dict[str, str]:
    return {key: "OK" if token in content else "NG" for key, token in KEYWORDS.items()}


def main() -> None:
    episode_files = list_episode_files(SOURCE_DIR)

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        output.write(f"EPxx.5 files: {len(episode_files)}\n")
        for file_path in episode_files:
            output.write(f"  {file_path.name}\n")
        output.write("\n")

        for file_path in episode_files:
            content = file_path.read_text(encoding="utf-8-sig", errors="replace")
            status = check_markers(content)
            found_themes = [theme for theme in THEMES if theme in content]

            output.write(f"--- {file_path.name} ---\n")
            output.write(f"  KW: {status['KW']}\n")
            output.write(f"  YT: {status['YT']}\n")
            output.write(f"  TN: {status['TN']}\n")
            output.write(f"  TH: {found_themes}\n")
            output.write(f"  RM: {status['RM']}\n\n")


if __name__ == "__main__":
    main()
