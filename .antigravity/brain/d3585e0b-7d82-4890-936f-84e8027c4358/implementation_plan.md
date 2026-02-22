# Implementation Plan - Manga System Refactoring

Refactor the Python-based Manga Generation System (`18_システム/*.py`) to improve maintainability, readability, and extensibility, while preserving the core functionality of updating manga prompts.

## User Review Required

> [!IMPORTANT]
> **Template Update**: The current system uses an old "2 Page" template. The refactoring will update this to the new **Continuous A4 Vertical** format established in EP06/EP07. This means running the new system on old files will update them to the new format (which is likely desired, but a significant change).

## Proposed Changes

### System Architecture

Refactor the monolithic script into modular components:

1. **`manga_core/models.py`**: Data structures (Pydantic or Dataclasses) for `MangaEpisode`, `MangaPanel`.
2. **`manga_core/template_manager.py`**: Handles loading templates from external files (Jinja2 or simple text).
3. **`manga_core/file_handler.py`**: Robust file I/O with `pathlib` and encoding handling.
4. **`manga_config.py`**: Pure configuration (Constants, Paths).

### File Changes

#### [NEW] [templates/manga_prompt.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/templates/manga_prompt.md)

Start using external template files instead of hardcoded strings. The new template will match the **EP06/EP07 High Quality style**:

- `((Vertical Portrait A4 Ratio))`
- `(Premium Digital Anime)`
- Strict Visual Locks

#### [MODIFY] [manga_utils.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/manga_utils.py)

- Improve Regex patterns to be more robust.
- Add proper error logging.

#### [MODIFY] [smart_refactor.py](file:///c:/Users/hirak/Desktop/2nd-Brain/18_システム/smart_refactor.py)

- usage of the new class-based structure.
- Ensure it can parse *both* old and new formats to extract dialogue safely.

## Verification Plan

### Automated Tests

- Run the refactored script on a **temporary test file** (not existing episodes) to verify it generates the correct markdown structure.
- Verify that "Visual Lock" variables are correctly substituted.

### Manual Verification

- Check if the output matches the confirmed style of EP06.
