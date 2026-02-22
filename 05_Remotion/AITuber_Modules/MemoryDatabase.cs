using UnityEngine;
using System.Collections.Generic;
using System.Linq;

public class MemoryDatabase : MonoBehaviour
{
    // 簡易的な記憶データ構造
    [System.Serializable]
    public class MemoryLog
    {
        public string key; // embeddingの代わり
        public string content;
        public System.DateTime timestamp;
    }

    private List<MemoryLog> longTermMemory = new List<MemoryLog>();

    /// <summary>
    /// メッセージに関連する記憶を検索して返す (RAGの簡易実装)
    /// </summary>
    public string RetrieveContext(string query)
    {
        // 本来はOpenAI Embeddings APIなどでベクトル化し、Cos類似度で検索する
        // ここではキーワードマッチでシミュレーション
        var related = longTermMemory
            .Where(m => query.Contains(m.key))
            .OrderByDescending(m => m.timestamp)
            .Take(3)
            .Select(m => m.content);

        if (!related.Any()) return "";

        return "【過去の記憶】\n" + string.Join("\n", related);
    }

    public void SaveMemory(string key, string content)
    {
        longTermMemory.Add(new MemoryLog 
        { 
            key = key, 
            content = content, 
            timestamp = System.DateTime.Now 
        });
    }
}
