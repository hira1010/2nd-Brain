using UnityEngine;
using UnityEngine.InputSystem; // Unityの新Input Systemのインポート

// 左右のフリッパーをHingeJoint2Dのモーターを使い物理的に回動させ、新Input Systemや音響・演出マネージャーと連携させるスクリプト
public class FlipperController : MonoBehaviour
{
    public enum FlipperSide { Left, Right }
    
    [Tooltip("フリッパーの左右区分")]
    public FlipperSide side;

    [Tooltip("フリッパーが跳ね上がる際のスプリングパワー")]
    public float hitStrength = 1800f; 
    
    [Tooltip("入力解除時に元に戻る際のスプリングパワー")]
    public float returnStrength = 700f;

    private HingeJoint2D hinge;
    private JointMotor2D jointMotor;
    private bool wasPressedLastFrame = false;

    void Start()
    {
        hinge = GetComponent<HingeJoint2D>();
        hinge.useMotor = true;
        jointMotor = hinge.motor;
    }

    void Update()
    {
        bool isPressed = false;
        
        // 新しい Input System のキーボードAPIを使ってキー入力を検知します
        if (Keyboard.current != null)
        {
            if (side == FlipperSide.Left)
            {
                // Aキーまたは左矢印キー
                isPressed = Keyboard.current.leftArrowKey.isPressed || Keyboard.current.aKey.isPressed;
            }
            else
            {
                // Dキーまたは右矢印キー
                isPressed = Keyboard.current.rightArrowKey.isPressed || Keyboard.current.dKey.isPressed;
            }
        }
        else
        {
            // もし新Input Systemがうまく認識されない場合の従来のインプットフォールバック
            if (side == FlipperSide.Left)
            {
                isPressed = Input.GetKey(KeyCode.LeftArrow) || Input.GetKey(KeyCode.A);
            }
            else
            {
                isPressed = Input.GetKey(KeyCode.RightArrow) || Input.GetKey(KeyCode.D);
            }
        }

        // キーが押された「瞬間」のみフリッパー駆動SEを再生
        if (isPressed && !wasPressedLastFrame)
        {
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.PlayFlipperMove();
            }
        }
        wasPressedLastFrame = isPressed;

        // ジョイントモーターの回動方向・速度設定
        if (isPressed)
        {
            // 左フリッパーは時計反り(負)、右は時計回り(正)へ急回転
            jointMotor.motorSpeed = (side == FlipperSide.Left) ? -hitStrength : hitStrength;
        }
        else
        {
            // キーを離したら元の初期ストッパー位置へ素早く戻します
            jointMotor.motorSpeed = (side == FlipperSide.Left) ? returnStrength : -returnStrength;
        }

        hinge.motor = jointMotor;
    }

    // フリッパーにボールが当たった瞬間の処理
    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Ball"))
        {
            Vector2 contactPoint = collision.transform.position;
            if (collision.contactCount > 0)
            {
                contactPoint = collision.GetContact(0).point;
            }
            
            // エフェクトマネージャーを介して、ヒット火花パーティクルを散らします
            if (EffectManager.Instance != null)
            {
                EffectManager.Instance.PlayHitEffect(contactPoint);
            }
        }
    }
}
