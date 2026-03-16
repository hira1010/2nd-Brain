/**
 * キャラクター表示コンポーネント（リファクタリング完全版）
 *
 * 機能:
 * - キャラクター画像の表示
 * - 口パクアニメーション
 * - 話している時の上下振動
 * - スライドイン登場アニメーション
 * - 表情差分の自動切り替え
 * - フォールバック画像表示
 */

import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { DEFAULT_CHARACTERS } from "../config";
import type { CharacterProps } from "../types/component.types";
import { SETTINGS } from "../settings.generated";
import { CHARACTER_CONSTANTS } from "../constants";
import { getCharacterImagePath } from "../utils/characterImageHelper";
import {
  calculateMouthState,
  calculateBounceY,
  calculateSlideIn,
} from "../utils/characterAnimation";

/**
 * キャラクターコンポーネント
 */
export const Character: React.FC<CharacterProps> = React.memo(
  ({ characterId, isSpeaking, emotion = "normal" }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    // キャラクター設定を取得
    const characterConfig = DEFAULT_CHARACTERS.find((c) => c.id === characterId);
    if (!characterConfig) {
      return null;
    }

    const isLeft = characterConfig.position === "left";

    // アニメーション計算
    const mouthOpen = calculateMouthState(frame, isSpeaking);
    const bounceY = calculateBounceY(frame, isSpeaking);
    const slideIn = calculateSlideIn(frame, fps, isLeft);

    // 画像パス取得
    const currentImage = getCharacterImagePath(characterId, emotion, mouthOpen);

    // 画像が有効かチェック
    const hasImage = SETTINGS.character.useImages;

    // スタイル
    const containerStyle: React.CSSProperties = {
      position: "absolute",
      bottom: 0,
      [characterConfig.position]: slideIn,
      transform: `translateY(${bounceY}px)`,
      transformOrigin: isLeft ? "bottom left" : "bottom right",
    };

    const imageStyle: React.CSSProperties = {
      height: CHARACTER_CONSTANTS.CHARACTER_HEIGHT,
      objectFit: "contain",
      transform: characterConfig.flipX ? "scaleX(-1)" : "none",
    };

    return (
      <div style={containerStyle}>
        {hasImage ? (
          <Img src={staticFile(currentImage)} style={imageStyle} />
        ) : (
          <CharacterPlaceholder
            characterId={characterId}
            characterConfig={characterConfig}
          />
        )}
      </div>
    );
  }
);

Character.displayName = "Character";

/**
 * キャラクタープレースホルダー
 * 画像がない場合の代替表示
 */
const CharacterPlaceholder: React.FC<{
  characterId: string;
  characterConfig: { name: string; color: string };
}> = React.memo(({ characterId, characterConfig }) => {
  const placeholderStyle: React.CSSProperties = {
    width: CHARACTER_CONSTANTS.PLACEHOLDER_WIDTH,
    height: CHARACTER_CONSTANTS.PLACEHOLDER_HEIGHT,
    background: `${characterConfig.color}20`,
    border: `${CHARACTER_CONSTANTS.PLACEHOLDER_BORDER_WIDTH}px solid ${characterConfig.color}`,
    borderRadius: CHARACTER_CONSTANTS.PLACEHOLDER_BORDER_RADIUS,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  };

  const emojiStyle: React.CSSProperties = {
    fontSize: CHARACTER_CONSTANTS.PLACEHOLDER_EMOJI_SIZE,
  };

  const nameStyle: React.CSSProperties = {
    fontSize: CHARACTER_CONSTANTS.PLACEHOLDER_TEXT_SIZE,
    fontWeight: "bold",
    color: characterConfig.color,
    marginTop: CHARACTER_CONSTANTS.PLACEHOLDER_TEXT_MARGIN_TOP,
  };

  const emoji = characterId === "zundamon" ? "🟢" : "🩷";

  return (
    <div style={placeholderStyle}>
      <div style={emojiStyle}>{emoji}</div>
      <div style={nameStyle}>{characterConfig.name}</div>
    </div>
  );
});

CharacterPlaceholder.displayName = "CharacterPlaceholder";
