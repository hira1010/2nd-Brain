# RenPy MCP + DevTools

**AI-powered MCP server and visual development tools for Ren'Py.**

Connect your AI assistant (Claude, etc.) directly to your Ren'Py project. Preview scenes, run tests, analyze story flow, manage translations, and live-debug your running game — all through natural language.

---

## Why RenPy MCP + DevTools?

Ren'Py is the most popular visual novel engine, but its development workflow is manual: edit scripts, launch game, click through scenes, check translations one file at a time. RenPy MCP + DevTools bridges that gap.

| Without | With RenPy MCP + DevTools |
|---|---|
| Manually launch game to check scenes | `screenshot_scene` captures any scene instantly |
| Click through entire game to test routes | `run_test` executes automated test cases |
| Search `.rpy` files with grep | `search_script` with regex across all scripts |
| Count translations by hand | `list_translations` shows completion % per language |
| Rename a character across 50 files | `rename_character` handles everything in one call |
| No way to inspect running game state | `live_get_state` shows variables, position, everything |

## Features

### 55 Tools in 9 Categories

**Project Management** — Set up, lint, compile, build, and inspect your project configuration.

**Visual Preview** — Screenshot any scene by warping to it. Generate gallery overviews of your entire game.

**Automated Testing** — Run Ren'Py test cases, create new tests, get pass/fail reports across all routes.

**Story Analysis** — Map character appearances, track variables, find dead ends, validate scripts, check dialogue consistency, search across all scripts with regex.

**Asset Management** — List images and audio, find unused assets, verify image dimensions match your game resolution.

**Refactoring** — Rename characters and labels across all files (with dry-run preview), extract story routes, insert dialogue at precise locations.

**Translation** — View completion status for all languages, find untranslated strings, generate translation templates, prepare entries for AI-assisted translation.

**Live Game Integration** — Connect to a running game via file-based IPC bridge. Evaluate expressions, inspect styles, read save files, take screenshots, jump to any label, set variables — all while the game runs.

**Documentation** — Search Ren'Py's official documentation (89 topics) directly from your AI assistant.

## Quick Start

### Prerequisites

- [Ren'Py SDK](https://www.renpy.org/latest.html) (8.x recommended)
- Python 3.11+
- An MCP-compatible AI client (Claude Desktop, Claude Code, etc.)

### Install

```bash
# Extract the zip, then:
cd renpy-mcp

# Install with uv (recommended)
uv venv && uv pip install -e .

# Or with pip
python -m venv .venv && .venv/Scripts/activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .
```

### Configure

Add to your MCP client configuration (e.g., `.mcp.json`):

```json
{
  "mcpServers": {
    "renpy-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/renpy-mcp",
        "renpy-mcp"
      ],
      "env": {
        "RENPY_SDK_PATH": "/path/to/renpy-sdk"
      }
    }
  }
}
```

### Use

Once connected, start by setting your project:

```
> Set my Ren'Py project to /path/to/my_game
> Show me the character map
> Take a screenshot of the "chapter2" scene
> How complete are the Japanese translations?
> Find all dialogue mentioning "love"
> Rename character "s" to "sylvie" (dry run first)
```

## Tool Reference

<details>
<summary><strong>Project (7 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `set_project` | Set the active Ren'Py project path |
| `get_project_info` | Get project structure (files, directories) |
| `lint_project` | Run Ren'Py lint for errors and warnings |
| `compile_project` | Compile `.rpy` scripts to `.rpyc` |
| `dump_project_metadata` | Export characters, labels, screens as JSON |
| `build_project` | Build distribution packages (PC, Mac, Linux, Web) |
| `package_info` | Show build configuration from `options.rpy` |

</details>

<details>
<summary><strong>Preview (3 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `screenshot_scene` | Warp to a script location and capture a screenshot |
| `list_warp_targets` | List all warpable locations in the project |
| `scene_preview_gallery` | Generate screenshots from multiple scenes |

</details>

<details>
<summary><strong>Testing (3 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `run_test` | Run Ren'Py automated test cases |
| `create_test` | Create a new test case file |
| `list_tests` | List all test cases in the project |

</details>

<details>
<summary><strong>Analysis (13 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `story_flow_graph` | Generate a story flow graph (labels, jumps, choices) |
| `find_dead_ends` | Find labels with no exit path |
| `track_variables` | Track variable definitions and usage |
| `count_dialogue` | Count dialogue lines per character |
| `character_map` | Map characters: definitions, dialogue counts, appearances |
| `validate_script` | Fast script validation (undefined refs, duplicate labels) |
| `playtest_report` | Run all test cases and generate a report |
| `generate_scene` | Generate a scene script template |
| `list_screens` | List all screen definitions with usage |
| `music_timeline` | Map music/sound across the story timeline |
| `search_script` | Regex search across all game scripts |
| `consistency_check` | Check dialogue consistency (spelling, length) |
| `accessibility_check` | Check for accessibility issues (alt text, contrast) |

</details>

<details>
<summary><strong>Assets (4 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `list_assets` | List all image assets |
| `find_unused_assets` | Find assets not referenced in scripts |
| `list_audio` | List audio files with script references |
| `image_size_check` | Verify image dimensions match game resolution |

</details>

<details>
<summary><strong>Refactoring (4 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `rename_character` | Rename a character variable across all files |
| `rename_label` | Rename a label and update all jump/call references |
| `extract_route` | Extract a complete story route to standalone script |
| `insert_dialogue` | Insert dialogue at a specific script location |

</details>

<details>
<summary><strong>Translation (7 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `list_translations` | List languages with completion percentage |
| `find_untranslated` | Find untranslated strings for a language |
| `translation_diff` | Show what changed since last translation update |
| `generate_translations` | Generate translation template files |
| `extract_translation_strings` | Export translatable strings to JSON |
| `merge_translation_strings` | Import translated strings from JSON |
| `auto_translate` | Prepare entries for AI-assisted translation |

</details>

<details>
<summary><strong>Live Integration (12 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `install_bridge` | Install the IPC bridge into your game |
| `uninstall_bridge` | Remove the bridge and IPC files |
| `live_ping` | Check if the running game is responding |
| `live_get_state` | Get current game state (variables, position) |
| `live_screenshot` | Capture the game as the player sees it |
| `live_eval` | Evaluate Python expressions in game context |
| `live_notify` | Show a notification in the running game |
| `live_jump` | Jump to any label in the running game |
| `live_set_variable` | Set a game variable at runtime |
| `style_inspector` | Inspect Ren'Py styles in the running game |
| `save_inspector` | Inspect save files and their metadata |
| `screen_hierarchy` | Inspect widget trees of shown screens |

</details>

<details>
<summary><strong>Documentation (2 tools)</strong></summary>

| Tool | Description |
|------|-------------|
| `search_docs` | Search Ren'Py documentation (89 topics) |
| `list_doc_topics` | List all available documentation topics |

</details>

## Architecture

```
AI Client (Claude)  <-->  MCP Protocol  <-->  RenPy MCP + DevTools
                                                    |
                                              +-----+-----+
                                              |           |
                                        RenPy CLI    File IPC
                                        (lint,       (bridge in
                                         test,       running game)
                                         warp)
```

**v1 — CLI Batch**: Lint, compile, test, warp+screenshot via `renpy.exe` subprocess.

**v2 — File-Based IPC**: A bridge script (`_mcp_bridge.rpy`) injected into the game polls `game/_mcp/cmd.json` for commands and writes responses to `status.json`. Uses `config.periodic_callbacks` for reliable polling even on the main menu.

## License

Proprietary. See [LICENSE](LICENSE) for details.
