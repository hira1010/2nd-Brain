using UnityEngine;
using DG.Tweening; // 伸縮ジャンプやしっぽのフリフリアニメーションを実現するDOTween

// 盤面中央にいる猫耳美少女キャラクターの表情切り替え、ジャンプ演出、しっぽの揺れを制御するスクリプト
public class PinballCharacterController : MonoBehaviour
{
    public static PinballCharacterController Instance { get; private set; }

    [Header("キャラクター表情スプライト設定")]
    [Tooltip("通常状態の表情")]
    public Sprite defaultFace;
    [Tooltip("笑顔（10万点、50万点などの時の表情）")]
    public Sprite smileFace;
    [Tooltip("ウインク顔（30万点などの時の表情）")]
    public Sprite winkFace;

    [Header("アニメーション対象パーツ参照")]
    [Tooltip("顔イラストを描いているSpriteRenderer")]
    public SpriteRenderer faceRenderer;
    [Tooltip("しっぽオブジェクトのTransform")]
    public Transform tailTransform;

    private Vector3 originalPosition;
    private Vector3 originalScale;
    private float expressionTimer = 0f;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // 伸縮アニメーション（Squash & Stretch）後に元に戻すための座標と大きさを保存します
        originalPosition = transform.position;
        originalScale = transform.localScale;

        // 表情を初期の通常顔にセット
        SetExpression(defaultFace);

        // 常時アニメーション：しっぽをゆらゆらとフリフリさせます
        StartTailWagging();
    }

    private void Update()
    {
        // 表情変化タイマーの更新
        if (expressionTimer > 0f)
        {
            expressionTimer -= Time.deltaTime;
            if (expressionTimer <= 0f)
            {
                // 一定時間経過したら自動で通常顔に戻します
                SetExpression(defaultFace);
            }
        }
    }

    // 表情を明示的に切り替えるメソッド
    public void SetExpression(Sprite faceSprite)
    {
        if (faceRenderer != null && faceSprite != null)
        {
            faceRenderer.sprite = faceSprite;
        }
    }

    // 笑顔を一定時間トリガーする処理
    public void TriggerSmile(float duration = 2.2f)
    {
        SetExpression(smileFace);
        expressionTimer = duration;
    }

    // ウインクを一定時間トリガーする処理
    public void TriggerWink(float duration = 1.3f)
    {
        SetExpression(winkFace);
        expressionTimer = duration;
    }

    // アニメーション表現：美少女がピョコッと愛らしくジャンプする処理
    public void Jump()
    {
        // 動作中のジャンプアニメーションを完全にリセット
        transform.DOComplete();
        transform.position = originalPosition;
        transform.localScale = originalScale;

        // ディズニーアニメなどで使われる「潰れて、伸びて、戻る」シーケンスを作成
        Sequence jumpSequence = DOTween.Sequence();
        
        // 1. 力をためる（縦に少し縮み、横に少し膨らむ）
        jumpSequence.Append(transform.DOScale(new Vector3(originalScale.x * 1.16f, originalScale.y * 0.78f, 1f), 0.08f));
        
        // 2. 上空へ飛び上がる（勢いで縦に引き伸ばされる）
        jumpSequence.Append(transform.DOMoveY(originalPosition.y + 1.4f, 0.24f).SetEase(Ease.OutQuad));
        jumpSequence.Join(transform.DOScale(new Vector3(originalScale.x * 0.84f, originalScale.y * 1.22f, 1f), 0.18f));

        // 3. 頂点付近で元の体型に戻る
        jumpSequence.Append(transform.DOScale(originalScale, 0.08f));

        // 4. 重力で地面に落下（着地）
        jumpSequence.Append(transform.DOMoveY(originalPosition.y, 0.22f).SetEase(Ease.InQuad));
        
        // 5. 着地の反動で再び少し潰れる
        jumpSequence.Append(transform.DOScale(new Vector3(originalScale.x * 1.12f, originalScale.y * 0.84f, 1f), 0.07f));
        // 6. 元の立ち姿に戻る
        jumpSequence.Append(transform.DOScale(originalScale, 0.1f));
    }

    // 常時しっぽをゆらゆらさせるDOTweenループ
    private void StartTailWagging()
    {
        if (tailTransform != null)
        {
            // しっぽをZ軸（角度）で左右にゆっくりと往復させます
            tailTransform.DOLocalRotate(new Vector3(0f, 0f, 12f), 1.3f)
                .SetEase(Ease.InOutSine)
                .SetLoops(-1, LoopType.Yoyo);
        }
    }
}
