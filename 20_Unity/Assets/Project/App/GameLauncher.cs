using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityMcpTextbook.View;

namespace UnityMcpTextbook.App
{
    [DisallowMultipleComponent]
    public sealed class GameLauncher : MonoBehaviour
    {
        private static GameLauncher current;
        private CancellationTokenSource flowCancellationTokenSource;
        private GameFlowController flowController;
        private bool initialized;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void Bootstrap()
        {
            EnsureInstance().Initialize();
        }

        private static GameLauncher EnsureInstance()
        {
            if (current != null)
            {
                return current;
            }

            current = FindFirstObjectByType<GameLauncher>();
            if (current != null)
            {
                return current;
            }

            var launcherObject = new GameObject(nameof(GameLauncher));
            DontDestroyOnLoad(launcherObject);
            current = launcherObject.AddComponent<GameLauncher>();
            return current;
        }

        public void Initialize()
        {
            if (initialized)
            {
                return;
            }

            Application.runInBackground = true;
            ConfigureMainCamera();
            EnsureEventSystem();
            EnsureAudioPlayer();

            var screens = GameScreenFactory.Create(transform);
            flowController = new GameFlowController(screens);
            flowCancellationTokenSource = new CancellationTokenSource();
            initialized = true;
            flowController.RunAsync(flowCancellationTokenSource.Token).Forget();
        }

        private void Awake()
        {
            if (current != null && current != this)
            {
                Destroy(gameObject);
                return;
            }

            current = this;
            DontDestroyOnLoad(gameObject);
            Initialize();
        }

        private void OnDestroy()
        {
            CancelFlow();
            flowController?.Dispose();
            flowController = null;

            if (RandomAudioPlayer.Instance != null)
            {
                RandomAudioPlayer.Instance.Dispose();
            }

            if (current == this)
            {
                current = null;
            }
        }

        private void CancelFlow()
        {
            flowCancellationTokenSource?.Cancel();
            flowCancellationTokenSource?.Dispose();
            flowCancellationTokenSource = null;
        }

        private void EnsureAudioPlayer()
        {
            if (RandomAudioPlayer.Instance != null)
            {
                return;
            }

            var audioPlayer = gameObject.AddComponent<RandomAudioPlayer>();
            audioPlayer.Initialize();
        }

        private static void EnsureEventSystem()
        {
            if (FindFirstObjectByType<EventSystem>() != null)
            {
                return;
            }

            var eventSystemObject = new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
            DontDestroyOnLoad(eventSystemObject);
        }

        private static void ConfigureMainCamera()
        {
            var mainCamera = Camera.main;
            if (mainCamera == null)
            {
                return;
            }

            mainCamera.clearFlags = CameraClearFlags.SolidColor;
            mainCamera.backgroundColor = Color.black;
        }
    }
}
