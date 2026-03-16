using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public enum AvatarState
{
    Idle,
    Listening,
    Thinking, // 新機能: 思考中
    Talking
}

public class AIAvatarController : MonoBehaviour
{
    [Header("PNGTuber Assets")]
    public Image avatarImage;
    public Sprite idleSprite;
    public Sprite thinkingSprite; // 思考中や目を回している画像など
    public Sprite talkingSpriteOpen;
    public Sprite talkingSpriteClosed;

    private AvatarState currentState = AvatarState.Idle;

    public void SetState(AvatarState state)
    {
        currentState = state;
        UpdateVisuals();
    }

    private void UpdateVisuals()
    {
        if (avatarImage == null) return;

        switch (currentState)
        {
            case AvatarState.Idle:
                if (idleSprite != null) avatarImage.sprite = idleSprite;
                // ここで呼吸アニメーションなどをTweenで入れるとリッチになります
                break;
            case AvatarState.Thinking:
                if (thinkingSprite != null) avatarImage.sprite = thinkingSprite;
                // 思考中は少し揺らす、明滅させるなどの演出
                break;
            // Listening, TalkingはLipsyncと連動
        }
    }

    public void Speak(string text)
    {
        StartCoroutine(LipSyncRoutine(text));
    }

    private IEnumerator LipSyncRoutine(string text)
    {
        // 簡易的なリップシンク（実際は音声解析やOVRを使う）
        float duration = text.Length * 0.1f;
        float timer = 0;
        
        while (timer < duration)
        {
            if (avatarImage != null && talkingSpriteOpen != null && talkingSpriteClosed != null)
            {
                avatarImage.sprite = (Time.time % 0.2f > 0.1f) ? talkingSpriteOpen : talkingSpriteClosed;
            }
            timer += Time.deltaTime;
            yield return null;
        }
        
        SetState(AvatarState.Idle);
    }
}
