# Implementation Plan - Remi Visual Update (Sanmenzu)

## Goal

Update Remi's visual description in all manga prompts (EP01-EP23) to strict "Sanmenzu" standards provided by the user (Red Suit, Black Lace High-neck, Red Skirt, Black Tights). Also ensure Yuto's "Blue Tie/White Shirt" consistency.

## Visual Standards

**Remi:**

- **(Silver Long Hair, Hime-cut)**
- **(Sharp Red Eyes, Cool Beauty Face)**
- **(Crimson Red Suit Jacket)**
- **(Black Lace High-neck Camisole)**
- **(Tight Red Skirt)**
- **(Black Pantyhose)**
- **(Black High Heels)**

**Yuto:**

- **(Short Black hair, slightly messy)**
- **(Navy Blue Suit)**
- **(White Shirt)**
- **(Blue Tie)**

## Proposed Changes

1. **Update `character_sheet.md`**: Establish the new source of truth.
2. **Batch Update Episodes**:
    - **Batch 1**: EP02 - EP09 (Re-verify and update "Camisole" to "High-neck Camisole" if needed).
    - **Batch 2**: EP10 - EP16 (Update visual locks).
    - **Batch 3**: EP17 - EP23 (Update visual locks).
    - **Batch 4**: Fractional Episodes (EP4.5, EP6.5, etc.).

## Verification Plan

- **Manual Review**: Randomly check 1 file from each batch to ensure the `multi_replace_file_content` worked correctly.
- **User Confirmation**: Notify user once all batches are processed.
