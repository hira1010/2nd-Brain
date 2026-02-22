# Refactoring Task

- [x] Analyze existing code
- [x] Create implementation plan
- [x] Refactor code
  - [x] Create `manga_config.py`
  - [x] Create `manga_utils.py`
  - [x] Update `generate_mangano.py`
  - [x] Update `fix_manga_prompts.py`
  - [x] Update `send_manga_email_final.py`
- [x] Fix encoding issue
  - [x] Root cause: `_ace_step.pth` with broken encoding
  - [x] Rewrite all files with Unicode escapes
- [x] Verify changes
  - [x] Run `generate_mangano.py` successfully (all 23 files generated)
