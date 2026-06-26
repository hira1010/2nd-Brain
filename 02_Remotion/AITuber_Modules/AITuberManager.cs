using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// AITuberシステム全体を統括するシングルトンマネージャー。
/// 他のコンポーネントへのアクセスポイントを提供します。
/// </summary>
public class AITuberManager : MonoBehaviour
{
    private static AITuberManager _instance;

    // シングルトンアクセサ
    public static AITuberManager Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = FindObjectOfType<AITuberManager>();
                if (_instance == null)
                {
                    GameObject obj = new GameObject("AITuberManager");
                    _instance = obj.AddComponent<AITuberManager>();
                }
            }
            return _instance;
        }
    }

    // サブシステムへの参照
    public MemoryDatabase Memory { get; private set; }
    public AIAvatarController Avatar { get; private set; }
    public LLMService LLM { get; private set; }

    [Header("State Debug")]
    public bool IsThinking;

    private void Awake()
    {
        // シングルトンの重複防止
        if (_instance != null && _instance != this)
        {
            Destroy(this.gameObject);
            return;
        }
        _instance = this;
        DontDestroyOnLoad(this.gameObject);

        // コンポーネントの初期化（本来はDI等を使うと良いが今回はシンプルに取得）
        Memory = GetComponentInChildren<MemoryDatabase>() ?? gameObject.AddComponent<MemoryDatabase>();
        Avatar = FindObjectOfType<AIAvatarController>();
        LLM = GetComponentInChildren<LLMService>() ?? gameObject.AddComponent<LLMService>();
    }

    /// <summary>
    /// AIへの質問処理を開始するメインフロー
    /// </summary>
    public void ProcessUserMessage(string userMessage)
    {
        StartCoroutine(ProcessFlow(userMessage));
    }

    private IEnumerator ProcessFlow(string message)
    {
        // 1. 記憶の検索 (RAG)
        string context = Memory.RetrieveContext(message);
        
        // 2. 思考中モーション開始
        IsThinking = true;
        if (Avatar != null) Avatar.SetState(AvatarState.Thinking);

        // 3. LLMへ送信 (Context含)
        // 実際のThinking表示（思考プロセス）のコールバックを受け取る想定
        yield return LLM.GenerateReply(message, context, (thinkingContent) => 
        {
            // Thinking中の途中経過表示などをフック
            Debug.Log($"Thinking... {thinkingContent}");
        }, 
        (finalResponse) => 
        {
            // 完了
            IsThinking = false;
            if (Avatar != null)
            {
                Avatar.SetState(AvatarState.Talking);
                Avatar.Speak(finalResponse);
            }
        });
    }
}
