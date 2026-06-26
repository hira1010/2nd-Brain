using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Cysharp.Threading.Tasks;

// ===== 設計理由 =====
// 層: View / Service
// 理由: PC上の指定フォルダから音声（.ogg）を動的にロードしてスピーカーから出力する処理は、
//       Unityのオーディオシステム（AudioSource）やOSへの依存（System.IO, UnityWebRequest）を伴う、
//       演出・ビュー関連の役割です。
// 責務:
//   - 初期化時に指定フォルダ内の音声ファイル一覧をスキャンし、パスを記憶する。
//   - 音声の再生が要求されたら、ランダムに1つのファイルを非同期でロードし、AudioSourceで再生する。
//   - インスタンス破棄時にリソースを適切に開放する（IDisposable実装）。
// =========================

namespace UnityMcpTextbook.View
{
    [DisallowMultipleComponent]
    public sealed class RandomAudioPlayer : MonoBehaviour, IDisposable
    {
        private const string AudioDirectory = @"C:\Users\hirak\Desktop\音声\音声";
        private readonly List<string> _audioFiles = new List<string>();
        private AudioSource _audioSource;

        /// <summary>
        /// 外部から簡単に呼び出せるようにするための静的（グローバル）なアクセス窓口です。
        /// </summary>
        public static RandomAudioPlayer Instance { get; private set; }

        /// <summary>
        /// 音声プレイヤーを初期化します。
        /// </summary>
        public void Initialize()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);

            // 音を鳴らすための Unity コンポーネントを追加
            _audioSource = gameObject.AddComponent<AudioSource>();
            LoadAudioFileList();
        }

        /// <summary>
        /// プレイヤーのリソースを開放します。
        /// </summary>
        public void Dispose()
        {
            if (Instance == this)
            {
                Instance = null;
            }
            _audioFiles.Clear();
        }

        private void OnDestroy()
        {
            Dispose();
        }

        /// <summary>
        /// 指定されたフォルダから .ogg 形式の音声ファイルをスキャンしてリストに保存します。
        /// </summary>
        private void LoadAudioFileList()
        {
            try
            {
                if (Directory.Exists(AudioDirectory))
                {
                    // フォルダ内のすべての .ogg ファイルの絶対パスを取得します
                    string[] files = Directory.GetFiles(AudioDirectory, "*.ogg");
                    _audioFiles.AddRange(files);
                    Debug.Log($"[RandomAudioPlayer] {AudioDirectory} から {_audioFiles.Count} 個の音声ファイルを読み込みました。");
                }
                else
                {
                    Debug.LogWarning($"[RandomAudioPlayer] 音声フォルダが見つかりません: {AudioDirectory}");
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"[RandomAudioPlayer] 音声ファイルの読み込み中にエラーが発生しました: {e.Message}");
            }
        }

        /// <summary>
        /// リストされた音声の中からランダムに1つを選び、非同期で読み込んで再生します。
        /// </summary>
        public async UniTask PlayRandomAsync()
        {
            if (_audioFiles.Count == 0)
            {
                return;
            }

            // ランダムに1つのファイルを決定
            int index = UnityEngine.Random.Range(0, _audioFiles.Count);
            string filePath = _audioFiles[index];

            // UnityWebRequest で読み込めるようにパスを整形 (例: file:///C:/Users/...)
            string fileUri = "file:///" + filePath.Replace('\\', '/');

            try
            {
                using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(fileUri, AudioType.OGGVORBIS))
                {
                    await www.SendWebRequest();

                    if (www.result == UnityWebRequest.Result.Success)
                    {
                        AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                        if (clip != null)
                        {
                            // 音を鳴らします（PlayOneShotを使うことで、音が重なっても途切れません）
                            _audioSource.PlayOneShot(clip);
                        }
                    }
                    else
                    {
                        Debug.LogError($"[RandomAudioPlayer] 音声のロードに失敗しました: {www.error} (URI: {fileUri})");
                    }
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"[RandomAudioPlayer] 再生エラー: {e.Message}");
            }
        }
    }
}
