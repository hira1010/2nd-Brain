# 設計判断
- 画面遷移はシーン分割せず、同一シーン内でのパネル（Canvas）の表示・非表示（SetActive）の切り替えで実装しました。
- 再スタート時のリセットを確実にするため、View（見た目）は保持したまま、Logic（計算）と Presenter（仲介役）を毎回新しく作り直しています。
- ボスモグラの追加にあたり、レイヤー間のアセンブリ依存関係（ViewがLogicに依存できない制約）を守るため、PresenterからViewへの情報受け渡しにはロジック用の `MoleType` 列挙型ではなく、単純な `bool`（ボスか通常か）を使用する設計としました。これにより、レイヤーの結合度を低く保ちつつ、ボス専用の演出（拡大、赤色化、HPテキスト表示）を実現しています。
- 毒モグラ（MoleType.Poison）追加にあたり、View層内に `MoleDisplayType` 列挙体（Normal/Boss/Poison）を新設し、Presenterが Logic の `MoleType` を `MoleDisplayType` に変換してViewへ渡す設計としました。これによりViewがLogic層のアセンブリに依存せずに3種類の外観を切り替えられます。
- ボスモグラのHP表示において、HP初期値（3）をViewにハードコードしていた実装を修正。LogicにGetCurrentHp()を追加し、OnMoleAppeared発火時にPresenterがLogicからHP値を取得してUpdateHpDisplay()でViewへ渡す形に変更しました。HP数値はゲーム状態なのでLogicが持ち、Viewは渡された数値を表示するだけの責務に限定しています。

