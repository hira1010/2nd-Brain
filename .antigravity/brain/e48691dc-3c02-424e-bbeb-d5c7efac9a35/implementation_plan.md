# Implementation Plan: Refactoring Manga Episodes

Existing episodes will be refactored to align with the standard format established in `EP06.4`. This ensures consistency in character visuals (Visual Locks) and prompt readability.

## User Review Required

> [!WARNING]
> **Corrupted Files Detected**
> The following files appear to have severe encoding issues (mojibake) and are currently unreadable:
>
> - `EP14_再生の緑_P66-70.md`
> - `EP16_落差の現実_P76-80.md`
> - `EP21_お金の旅路_P101-105.md`
>
> **I will NOT modify these files** to prevent further data loss. I will focus the refactoring on the readable files listed below.

## Proposed Changes

Standardize Visual Locks, Panel formatting (spacing), and Negative Prompts.

### Target Files

#### [MODIFY] [EP07_苗木を植える_P31-35.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/%E5%AE%8C%E6%88%90%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80/EP07_%E8%8B%97%E6%9C%A8%E3%82%92%E6%A4%8D%E3%81%88%E3%82%8B_P31-35.md)

- Update Remi Visual Lock.
- Update Yuto Visual Lock.
- Add spacing between panels.
- Clean up Negative Prompt.

#### [MODIFY] [EP03_誘惑の囁き_P11-15.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/%E5%AE%8C%E6%88%90%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80/EP03_%E8%AA%98%E6%83%91%E3%81%AE%E5%9B%81%E3%81%8D_P11-15.md)

- Standardize Visual Locks and formatting.

#### [MODIFY] [EP20.5_自由の定義.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/01_%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC/EP20.5_%E8%87%AA%E7%94%B1%E3%81%AE%E5%AE%9A%E7%BE%A9.md)

- Standardize Visual Locks and formatting.

#### [MODIFY] [EP14_再生の緑_P66-70.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/01_%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC/EP14_%E5%86%8D%E7%94%9F%E3%81%AE%E7%B7%91_P66-70.md)

- Update Visual Locks despite encoding issues (User Override).
- Standardize formatting.

#### [MODIFY] [EP16_落差の現実_P76-80.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/01_%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC/EP16_%E8%90%BD%E5%B7%AE%E3%81%AE%E7%8F%BE%E5%AE%9F_P76-80.md)

- Update Visual Locks despite encoding issues (User Override).
- Standardize formatting.

#### [MODIFY] [EP21_お金の旅路_P101-105.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/01_%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC/EP21_%E3%81%8A%E9%87%91%E3%81%AE%E6%97%85%E8%B7%AF_P101-105.md)

- Update Visual Locks despite encoding issues (User Override).
- Standardize formatting.

#### [MODIFY] [EP08_積立の開始_P36-40.md](file:///c:/Users/hirak/Desktop/2nd-Brain/18_%E3%83%AC%E3%83%9F%E6%8A%95%E8%B3%87%E6%BC%AB%E7%94%BB/%E3%83%9E%E3%83%B3%E3%82%AC%E3%83%8E/01_%E9%95%B7%E7%B7%A8_%E5%B8%8C%E6%9C%9B%E3%81%AE%E6%8A%95%E8%B3%87/%E5%AE%8C%E6%88%90%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80/EP08_%E7%A9%8D%E7%AB%8B%E3%81%AE%E9%96%8B%E5%A7%8B_P36-40.md)

- Standardize Remi/Yuto Visual Locks.
- Apply consistent panel formatting.

> [!WARNING]
> **Read Error: EP22_自分自身の道_P106-110.md**
> Unable to read this file due to an encoding or format issue ("unsupported mime type"). Please check if the file is open in another program or has a special encoding. Skipping for now.

## Verification Plan

### Manual Verification

- Review the modified files to ensure the Visual Locks are identical to the standard defined in `EP06.4`.
- Check that no narrative content (Speech Bubbles, Plot) has been altered, only formatting and visual descriptors.
