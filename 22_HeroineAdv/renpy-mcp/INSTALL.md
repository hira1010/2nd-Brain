# RenPy MCP + DevTools — Installation Guide

## Prerequisites

1. **Ren'Py SDK 8.x** — Download from https://www.renpy.org/latest.html
2. **Python 3.11+** — https://www.python.org/downloads/
3. **uv** (recommended) — https://docs.astral.sh/uv/getting-started/installation/
4. **MCP-compatible AI client** — Claude Code, Claude Desktop, or any MCP client

## Step 1: Extract

Extract this zip to a permanent location. For example:

- Windows: `C:\Tools\renpy-mcp`
- macOS/Linux: `~/tools/renpy-mcp`

## Step 2: Install dependencies

Open a terminal in the extracted folder and run:

```bash
# With uv (recommended)
uv venv
uv pip install -e .

# Or with pip
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e .
```

## Step 3: Configure your AI client

### Claude Code

Create a `.mcp.json` file in your project directory (or in the folder where you run Claude Code):

```json
{
  "mcpServers": {
    "renpy-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "C:/Tools/renpy-mcp",
        "renpy-mcp"
      ],
      "env": {
        "RENPY_SDK_PATH": "C:/path/to/renpy-8.x-sdk"
      }
    }
  }
}
```

Replace the paths:
- `--directory` → where you extracted this zip
- `RENPY_SDK_PATH` → your Ren'Py SDK folder (the one containing `renpy.exe` or `renpy.sh`)

### Claude Desktop

Add the same config to your Claude Desktop settings:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Step 4: Use

### Option A: Visual DevTools (no AI needed)

Run from the renpy-mcp directory:

```bash
# With uv
uv run renpy-webui -p /path/to/my-game

# Or with venv activated
renpy-webui -p /path/to/my-game
```

This opens the web dashboard in your browser with Story Map, Dev Dashboard, Script Editor, Heatmap, and Asset Manager.

Options:
- `-p` / `--project` — Path to your Ren'Py project (required)
- `--page` — Start page: `/dashboard`, `/story-map`, `/script-editor`, `/heatmap`, `/assets` (default: `/dashboard`)
- `--port` — Port number (default: auto)
- `--no-browser` — Don't open browser automatically

For live features (game preview, variable inspector, warp-on-click), start your Ren'Py game with the bridge installed. The bridge can be installed via the MCP `install_bridge` tool, or by copying `src/renpy_mcp/bridge/bridge_script.rpy` to your game directory as `_mcp_bridge.rpy`.

### Option B: AI-Powered (MCP)

Start your AI client and try:

```
Set my Ren'Py project to C:/path/to/my_game
```

Then ask anything:

```
Show me the story flow graph and find any dead ends
Who are the characters and how much dialogue does each have?
Screenshot the scene where Sylvie appears at the library
How complete are the Japanese translations?
Rename character "s" to "sylvie" — dry run first
Lint the project and check for consistency issues
Search the Ren'Py docs for "screen language"
```

## Troubleshooting

### "command not found: uv"
Install uv first: https://docs.astral.sh/uv/getting-started/installation/

### "RENPY_SDK_PATH not set"
Make sure the `env` section in your MCP config points to a valid Ren'Py SDK directory.

### Tools are not showing up
Restart your AI client after saving the `.mcp.json` config file.

### Screenshot fails / game window flashes
This is normal — `screenshot_scene` launches Ren'Py in a headless-like mode to capture the frame, then closes automatically.

## Links

- Website: https://renpy-mcp.abyo.net/
- itch.io: https://y1uda.itch.io/renpy-mcp
- Discord: https://discord.gg/N6sSHBGuYX
