using UnityEngine;
using UnityEngine.UI;
using UnityMcpTextbook.View;

namespace UnityMcpTextbook.App
{
    internal static class GameScreenFactory
    {
        private static readonly Vector2[] HolePositions =
        {
            new(-250f, 150f),
            new(0f, 150f),
            new(250f, 150f),
            new(-250f, -130f),
            new(0f, -130f),
            new(250f, -130f),
            new(-250f, -410f),
            new(0f, -410f),
            new(250f, -410f),
        };

        public static GameScreenRefs Create(Transform parent)
        {
            var titleCanvas = CreateTitleScreen(parent, out var startButton);
            var gameplayCanvas = CreateGameplayScreen(parent, out var holeViews);
            var scoreCanvas = CreateScoreScreen(parent, out var scoreView);
            var timerCanvas = CreateTimerScreen(parent, out var timerView);
            var resultCanvas = CreateResultScreen(parent, out var retryButton, out var titleButton, out var resultScoreText);

            return new GameScreenRefs(
                titleCanvas,
                gameplayCanvas,
                scoreCanvas,
                timerCanvas,
                resultCanvas,
                startButton,
                retryButton,
                titleButton,
                resultScoreText,
                scoreView,
                timerView,
                holeViews);
        }

        private static GameObject CreateTitleScreen(Transform parent, out Button startButton)
        {
            var titleCanvas = UIFactory.CreateOverlayCanvas(parent, "TitleCanvas", 5);
            var titleBg = UIFactory.CreateChildImage(titleCanvas.transform, "Background", new Vector2(1080, 1920), Vector2.zero, false);
            titleBg.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Textures/title_background.png");

            var startButtonImage = UIFactory.CreateChildImage(titleCanvas.transform, "StartButton", new Vector2(300, 100), new Vector2(0, -500), true);
            startButtonImage.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_start.png");
            startButton = startButtonImage.gameObject.AddComponent<Button>();

            var startText = UIFactory.CreateOverlayText(startButtonImage.transform, "Text", Vector2.zero, 40, Color.white, "START");
            UIFactory.MakeCenter(startText.rectTransform);
            return titleCanvas;
        }

        private static GameObject CreateGameplayScreen(Transform parent, out MoleHoleView[] holeViews)
        {
            var gameplayCanvas = UIFactory.CreateGameplayCanvas(parent);
            UIFactory.CreateStageBackground(gameplayCanvas.transform);

            holeViews = new MoleHoleView[HolePositions.Length];
            for (var i = 0; i < HolePositions.Length; i++)
            {
                holeViews[i] = UIFactory.CreateDefaultMoleHoleView(gameplayCanvas.transform, i, HolePositions[i]);
            }

            return gameplayCanvas;
        }

        private static GameObject CreateScoreScreen(Transform parent, out ScoreView scoreView)
        {
            var scoreCanvas = UIFactory.CreateOverlayCanvas(parent, "ScoreCanvas", 10);
            Object.Destroy(scoreCanvas.GetComponent<GraphicRaycaster>());

            var scoreText = UIFactory.CreateOverlayText(scoreCanvas.transform, "ScoreText", new Vector2(0f, -220f), 64, Color.white, "スコア: 0");
            scoreView = scoreCanvas.AddComponent<ScoreView>();
            scoreView.SetTextTarget(scoreText);
            return scoreCanvas;
        }

        private static GameObject CreateTimerScreen(Transform parent, out TimerView timerView)
        {
            var timerCanvas = UIFactory.CreateOverlayCanvas(parent, "TimerCanvas", 10);
            Object.Destroy(timerCanvas.GetComponent<GraphicRaycaster>());

            var timerText = UIFactory.CreateOverlayText(timerCanvas.transform, "TimerText", new Vector2(0f, -96f), 72, new Color(1f, 0.92f, 0.35f), "のこりじかん: 60");
            timerView = timerCanvas.AddComponent<TimerView>();
            timerView.SetTextTarget(timerText);
            return timerCanvas;
        }

        private static GameObject CreateResultScreen(Transform parent, out Button retryButton, out Button titleButton, out Text resultScoreText)
        {
            var resultCanvas = UIFactory.CreateOverlayCanvas(parent, "ResultCanvas", 20);
            var resultBg = UIFactory.CreateChildImage(resultCanvas.transform, "Background", new Vector2(1080, 1920), Vector2.zero, true);
            resultBg.color = new Color(0, 0, 0, 0.75f);
            resultBg.sprite = null;

            UIFactory.CreateOverlayText(resultCanvas.transform, "Title", new Vector2(0, -300), 80, Color.white, "RESULT");
            resultScoreText = UIFactory.CreateOverlayText(resultCanvas.transform, "Score", new Vector2(0, -500), 100, Color.yellow, "スコア: 0");

            var retryButtonImage = UIFactory.CreateChildImage(resultCanvas.transform, "RetryButton", new Vector2(300, 100), new Vector2(0, -800), true);
            retryButtonImage.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_retry.png");
            retryButton = retryButtonImage.gameObject.AddComponent<Button>();
            var retryText = UIFactory.CreateOverlayText(retryButtonImage.transform, "Text", Vector2.zero, 30, Color.white, "もう一度");
            UIFactory.MakeCenter(retryText.rectTransform);

            var titleButtonImage = UIFactory.CreateChildImage(resultCanvas.transform, "TitleButton", new Vector2(300, 100), new Vector2(0, -950), true);
            titleButtonImage.sprite = UIFactory.LoadEditorSprite("Assets/Project/Images/Atlas/btn_title.png");
            titleButton = titleButtonImage.gameObject.AddComponent<Button>();
            var titleText = UIFactory.CreateOverlayText(titleButtonImage.transform, "Text", Vector2.zero, 30, Color.white, "タイトルへ");
            UIFactory.MakeCenter(titleText.rectTransform);

            return resultCanvas;
        }
    }
}
