using UnityEngine;

// プレイヤーのハイスコアをセーブ・ロードするマネージャー（静的クラス風に動作）
public class SaveManager : MonoBehaviour
{
    private const string HighScoreKey = "Pinball_HighScore";

    // ハイスコアを保存する処理
    public static void SaveHighScore(int score)
    {
        int currentHighScore = LoadHighScore();
        if (score > currentHighScore)
        {
            PlayerPrefs.SetInt(HighScoreKey, score);
            PlayerPrefs.Save();
            Debug.Log($"[SaveManager] 新しいハイスコアを保存しました: {score}");
        }
    }

    // ハイスコアを読み込む処理
    public static int LoadHighScore()
    {
        return PlayerPrefs.GetInt(HighScoreKey, 0);
    }

    // デバッグ用にスコアを初期化する処理
    public static void ResetHighScore()
    {
        PlayerPrefs.DeleteKey(HighScoreKey);
        PlayerPrefs.Save();
        Debug.Log("[SaveManager] ハイスコアを初期化しました。");
    }
}
