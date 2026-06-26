# Core_共通テンプレ.md - プログラムの土台

このファイルは、新しくゲームのプログラム（C#スクリプトなど）を書く際の、ベースとなるコードの型（テンプレート）を置いておく場所です。

## 📄 基本の型（例：画面の制御）

```csharp
using UnityEngine;

/// <summary>
/// 画面の表示や演出を管理するクラス（View）
/// </summary>
public class BaseView : MonoBehaviour
{
    // ここに共通の処理（画面のフェードイン・アウトなど）を書く
    
    public virtual void Initialize()
    {
        // 初期化処理
    }
}
```

## 📄 基本の型（例：ゲームのルール）

```csharp
/// <summary>
/// ゲームのルールや点数などを管理するクラス（Logic）
/// </summary>
public class BaseLogic
{
    protected int score = 0;
    
    public virtual void AddScore(int value)
    {
        score += value;
    }
}
```

※作成するゲームのジャンルに合わせて、AIにこの型をベースにするよう指示してください。
