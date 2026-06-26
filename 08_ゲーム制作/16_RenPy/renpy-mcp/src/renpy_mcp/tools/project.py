"""Project management tools."""

import json
import re
from pathlib import Path

from mcp.server.fastmcp import Context

from ..config import RenPyConfig
from ..renpy_runner import RenPyRunner


def register_project_tools(mcp, config: RenPyConfig, runner: RenPyRunner):
    """Register project-related MCP tools."""

    @mcp.tool()
    async def set_project(path: str) -> str:
        """Set the active RenPy project path.

        Args:
            path: Absolute path to the RenPy project directory.
        """
        project = Path(path)
        game_dir = project / "game"
        if not project.exists():
            return f"Error: Path does not exist: {path}"
        if not game_dir.exists():
            return f"Error: Not a valid RenPy project (no 'game' directory): {path}"
        config.project_path = project
        return f"Project set to: {path}"

    @mcp.tool()
    async def get_project_info() -> str:
        """Get information about the current RenPy project structure.

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."

        game_dir = config.project_path / "game"
        info = {
            "project_path": str(config.project_path),
            "game_dir": str(game_dir),
            "rpy_files": [],
            "image_dirs": [],
            "audio_dirs": [],
        }

        if game_dir.exists():
            for f in sorted(game_dir.rglob("*.rpy")):
                info["rpy_files"].append(str(f.relative_to(config.project_path)))

            for subdir in ["images", "gui"]:
                d = game_dir / subdir
                if d.exists():
                    info["image_dirs"].append(str(d.relative_to(config.project_path)))

            for subdir in ["audio", "music", "sfx", "sound"]:
                d = game_dir / subdir
                if d.exists():
                    info["audio_dirs"].append(str(d.relative_to(config.project_path)))

        return json.dumps(info, indent=2, ensure_ascii=False)

    @mcp.tool()
    async def lint_project() -> str:
        """Run RenPy lint to check the project for errors and warnings.

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."
        return await runner.lint()

    @mcp.tool()
    async def compile_project() -> str:
        """Compile RenPy scripts (.rpy -> .rpyc).

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."
        return await runner.compile()

    @mcp.tool()
    async def dump_project_metadata() -> str:
        """Dump project metadata (characters, labels, screens, etc.) to JSON.

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."
        output_file = await runner.json_dump()
        if output_file.exists():
            return output_file.read_text(encoding="utf-8")
        return "Error: JSON dump was not created."

    @mcp.tool()
    async def build_project(
        formats: str = "pc,mac",
        destination: str = "",
    ) -> str:
        """Build the project for distribution.

        Args:
            formats: Comma-separated build formats. Options: pc, mac, linux, web, all.
            destination: Output directory for builds (default: project/builds/).

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."

        if not destination:
            dest_dir = config.project_path / "builds"
            dest_dir.mkdir(exist_ok=True)
            destination = str(dest_dir)

        # RenPy uses the launcher to build distributions
        # The command is: renpy.exe launcher distribute <project> --destination <dest>
        try:
            args = ["distribute", str(config.project_path), "--destination", destination]
            if formats != "all":
                # Map format names to RenPy package types
                format_map = {
                    "pc": "pc",
                    "win": "pc",
                    "windows": "pc",
                    "mac": "mac",
                    "linux": "linux",
                    "web": "web",
                    "android": "android",
                }
                for fmt in formats.split(","):
                    fmt = fmt.strip().lower()
                    if fmt in format_map:
                        args.extend(["--package", format_map[fmt]])

            result = await runner.run_command(
                *args,
                project_path=config.sdk_path / "launcher",
                timeout=300.0,
            )
            output = result.stdout + result.stderr
            if result.returncode == 0:
                return f"Build completed successfully.\nOutput: {destination}\n\n{output[:1000]}"
            return f"Build failed (exit code {result.returncode}):\n{output[:2000]}"
        except Exception as e:
            return f"Build error: {e}"

    @mcp.tool()
    async def package_info() -> str:
        """Show build/packaging configuration from the project.

        Reads build classification rules, file patterns, and
        distribution settings from options.rpy.

        Requires set_project to be called first.
        """
        if not config.project_path:
            return "Error: No project set. Use set_project first."

        game_dir = config.project_path / "game"
        options_file = game_dir / "options.rpy"

        if not options_file.exists():
            return "Error: options.rpy not found."

        try:
            content = options_file.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading options.rpy: {e}"

        info = {
            "config_values": {},
            "build_rules": [],
        }

        # Extract config values
        config_re = re.compile(r'^\s*define\s+(config\.\w+|build\.\w+)\s*=\s*(.+)')
        build_classify_re = re.compile(r'^\s*build\.classify\s*\(\s*["\'](.+?)["\']\s*,\s*["\'](.+?)["\']\s*\)')

        for line in content.splitlines():
            m = config_re.match(line)
            if m:
                key = m.group(1)
                value = m.group(2).strip()
                info["config_values"][key] = value

            m = build_classify_re.match(line)
            if m:
                info["build_rules"].append({
                    "pattern": m.group(1),
                    "target": m.group(2),
                })

        return json.dumps(info, indent=2, ensure_ascii=False)
