using UnityEngine;
using System;
using System.Collections;

public class LLMService : MonoBehaviour
{
    [Header("Model Settings")]
    public string modelName = "deepseek-r1"; // 新しいモデル
    public bool showThinkingProcess = true;

    /// <summary>
    /// LLMへリクエストを送る
    /// </summary>
    /// <param name="onThinkingUpdate">Thinkingプロセスが出力された時のコールバック</param>
    /// <param name="onComplete">最終回答のコールバック</param>
    public IEnumerator GenerateReply(string prompt, string context, Action<string> onThinkingUpdate, Action<string> onComplete)
    {
        // ここで実際のAPIコールを行う (HTTP Request)
        
        // --- モック処理開始 ---
        
        // Thinkingプロセスのシミュレーション
        if (showThinkingProcess)
        {
            string[] thinkingSteps = {
                "ユーザーの意図を解析中...",
                "過去のメモリと照合中...",
                "適切な回答トーンを生成中..."
            };

            foreach (var step in thinkingSteps)
            {
                onThinkingUpdate?.Invoke(step);
                yield return new WaitForSeconds(0.5f); // 思考時間の演出
            }
        }

        // 回答生成
        string response = $"こんにちは！その質問については、{context} ということを覚えていますよ。";
        onComplete?.Invoke(response);
        
        // --- モック処理終了 ---
    }
}
