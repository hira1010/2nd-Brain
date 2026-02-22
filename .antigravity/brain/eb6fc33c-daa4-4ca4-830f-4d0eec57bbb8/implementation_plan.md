# Refactoring & Prompt Fix Plan

## Goal Description
1. **Fix Generation Prompt**: The AI is still treating the "Backup" data as passive context. I will modify the "Backup" prompt to *explicitly command* the AI to generate Page 1 immediately if no other instruction is given, or completely change the header to look like a "Start Generation" command rather than a "Backup".
2. **Refactor Codebase**: Execute the previously approved refactoring plan (delete `mangaCore.js`, split `useMangaState.js`).

## User Review Required
None.

## Proposed Changes

### 1. Harder Prompt Fix
#### [MODIFY] [src/utils/manga/prompt/generator.js](file:///c:/Users/hirak/Desktop/%E6%BC%AB%E7%94%BB/src/utils/manga/prompt/generator.js)
- Change header from "Project Backup" to "Project Context & Action Trigger".
- Add explicit instruction: "IMMEDIATELY START GENERATING PAGE 1 using the data below. Do not wait for confirmation."

### 2. Simplify `utils/manga/` (Refactoring)
#### [DELETE] [src/utils/manga/mangaCore.js](file:///c:/Users/hirak/Desktop/%E6%BC%AB%E7%94%BB/src/utils/manga/mangaCore.js)
- Delete redundant file.

#### [MODIFY] [src/utils/manga/layoutGenerator.js](file:///c:/Users/hirak/Desktop/%E6%BC%AB%E7%94%BB/src/utils/manga/layoutGenerator.js)
- Update imports.

### 3. Refactor State Management (`hooks/`) (Refactoring)
#### [NEW] [src/hooks/usePersistence.js](file:///c:/Users/hirak/Desktop/%E6%BC%AB%E7%94%BB/src/hooks/usePersistence.js)
- Extract persistence logic.

#### [MODIFY] [src/hooks/useMangaState.js](file:///c:/Users/hirak/Desktop/%E6%BC%AB%E7%94%BB/src/hooks/useMangaState.js)
- Use `usePersistence`.

## Verification Plan
### Automated Tests
- Run `npm run build`.
- Run `node reproduce_issue.js`.

### Manual Verification
- Check generated prompt text to ensure it contains the new imperative commands.
