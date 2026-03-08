# 20_AI生成 (AI Generation)

このフォルダは、Stability Matrixおよびその他のAI生成ツールを管理・操作するための場所です。

## 📁 構成

- `stability_matrix_controller.py`: Stability Matrixを操作するためのPythonスクリプト
- `README.md`: このファイル

## 🚀 Stability Matrixの操作

### 起動

以下のコマンドで、Stability Matrixをバックグラウンドで起動できます。

```powershell
python 20_AI生成/stability_matrix_controller.py --start
```

### 状態確認

現在Stability Matrixが起動しているかどうかを確認します。

```powershell
python 20_AI生成/stability_matrix_controller.py --status
```

## 🛠️ 設定の変更

Stability Matrixの実行ファイル（`.exe`）の場所を変更した場合は、以下のファイルを編集してください。

- `lib/config.py` 内の `STABILITY_MATRIX_EXE` 定数

現在の設定パス: `c:\Users\hirak\Desktop\StabilityMatrix.exe`

## 📝 補足

- Stability Matrixのデータ（モデルやパッケージ）は `C:\Users\hirak\AppData\Roaming\StabilityMatrix` に保存されています。
- このフォルダに、AI生成に関するワークフローや生成スクリプトを順次追加していきます。
