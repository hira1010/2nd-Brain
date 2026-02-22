# Global Skill Implementation Plan: Manzai Video Generation

## Goal Description

The user is currently manually running `generate_manzai_audio.py` to create audio for their "Remi Investment Manga" manzai videos. To streamline this and make it a "Global Skill", I propose refactoring the script into a reusable system tool and creating a workflow that can be executed from anywhere in the workspace.

## User Review Required
>
> [!IMPORTANT]
>
> - I will be moving the core logic of `generate_manzai_audio.py` to `_system_scripts/manzai/generate_audio.py` (or similar) to make it globally accessible.
> - I will create a new workflow file `.agent/workflows/manzai-gen.md`.
> - Please confirm if you want to extend this to include **Video Generation** (merging audio with images) if I can find the logic or if you have a preferred way (e.g., Remotion or MoviePy). For now, I will focus on Audio.

## Proposed Changes

### System Scripts

#### [NEW] [generate_manzai_audio.py](file:///c:/Users/hirak/Desktop/2nd-Brain/_system_scripts/generate_manzai_audio.py)

- Refactor the existing script to accept arguments (input file, output directory) so it can be called from any location.
- Enhance error handling and API key management (ensure it reads from env).

### Workflows

#### [NEW] [manzai-gen.md](file:///c:/Users/hirak/Desktop/2nd-Brain/.agent/workflows/manzai-gen.md)

- Define a workflow that:
    1. Asks for the input Markdown script path.
    2. Asks for the output directory (defaulting to current `audio` folder).
    3. Runs the `_system_scripts/generate_manzai_audio.py`.
    4. (Optional) Asks if the user wants to generate a video (if we add that step).

## Verification Plan

### Automated Tests

- None for the script itself (requires API key).
- I will run the script with a `--dry-run` or similar flag if implemented, or checking help output.

### Manual Verification

- Run the new workflow `manzai-gen` on the existing `Manzai_Script_60sec.md` and verify it generates audio (or at least attempts to, if API key is set).
- Check if the output files are created in the correct directory.
