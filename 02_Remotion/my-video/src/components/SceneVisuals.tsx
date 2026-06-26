/**
 * シーンビジュアル表示コンポーネント（完全版）
 *
 * 機能:
 * - リアリティ画像の表示
 * - Ken Burns エフェクト（ゆっくりズーム）
 * - テキストオーバーレイ表示
 * - 各種アニメーション効果
 */

import React from "react";
import { Img, staticFile } from "remotion";
import type { SceneVisualsProps } from "../types/component.types";
import { useAnimationStyle } from "../hooks/useAnimationStyle";
import { useKenBurnsEffect } from "../hooks/useKenBurnsEffect";
import { ANIMATION_CONSTANTS, VISUAL_CONSTANTS, PATH_CONSTANTS } from "../constants";

/**
 * シーンビジュアルコンポーネント
 *
 * @param frame - 現在のフレーム（シーン内の相対位置）
 * @param fps - フレームレート
 * @param visual - 表示するビジュアルコンテンツ
 */
import { getImagePath } from "../utils/path";

/**
 * シーンビジュアルコンポーネント
 *
 * @param frame - 現在のフレーム（シーン内の相対位置）
 * @param fps - フレームレート
 * @param visual - 表示するビジュアルコンテンツ
 */
export const SceneVisuals: React.FC<SceneVisualsProps> = React.memo(
  ({ frame, fps, visual }) => {
    // アニメーションスタイル計算
    const animationStyle = useAnimationStyle({
      frame,
      fps,
      animation: visual?.animation,
    });

    // Ken Burns エフェクト計算
    const kenBurnsScale = useKenBurnsEffect({
      frame,
      fps,
      duration: ANIMATION_CONSTANTS.KEN_BURNS_DURATION,
      startScale: ANIMATION_CONSTANTS.KEN_BURNS_START_SCALE,
      endScale: ANIMATION_CONSTANTS.KEN_BURNS_END_SCALE,
    });

    // コンテンツコンテナスタイル
    const contentContainer: React.CSSProperties = {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden", // Ken Burns効果ではみ出しをカット
      ...animationStyle,
    };

    // ビジュアルがない場合
    if (!visual || visual.type === "none") {
      return null;
    }

    // 画像表示 (Reality & Ken Burns)
    if (visual.type === "image" && visual.src) {
      const imagePath = getImagePath(visual.src);

      return (
        <div style={contentContainer}>
          <Img
            src={staticFile(imagePath)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${kenBurnsScale})`,
            }}
          />
        </div>
      );
    }

    // テキスト表示
    if (visual.type === "text" && visual.text) {
      const textStyle: React.CSSProperties = {
        fontSize: visual.fontSize || VISUAL_CONSTANTS.DEFAULT_TEXT_SIZE,
        fontWeight: "bold",
        color: visual.color || VISUAL_CONSTANTS.DEFAULT_TEXT_COLOR,
        textAlign: "center",
        lineHeight: VISUAL_CONSTANTS.TEXT_LINE_HEIGHT,
        whiteSpace: "pre-wrap",
        textShadow: VISUAL_CONSTANTS.TEXT_SHADOW,
      };

      return (
        <div style={contentContainer}>
          <div style={textStyle}>{visual.text}</div>
        </div>
      );
    }

    return null;
  }
);

SceneVisuals.displayName = "SceneVisuals";
