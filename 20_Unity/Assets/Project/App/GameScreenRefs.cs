using UnityEngine;
using UnityEngine.UI;
using UnityMcpTextbook.View;

namespace UnityMcpTextbook.App
{
    internal sealed class GameScreenRefs
    {
        public GameScreenRefs(
            GameObject titleCanvas,
            GameObject gameplayCanvas,
            GameObject scoreCanvas,
            GameObject timerCanvas,
            GameObject resultCanvas,
            Button startButton,
            Button retryButton,
            Button titleButton,
            Text resultScoreText,
            ScoreView scoreView,
            TimerView timerView,
            MoleHoleView[] holeViews)
        {
            TitleCanvas = titleCanvas;
            GameplayCanvas = gameplayCanvas;
            ScoreCanvas = scoreCanvas;
            TimerCanvas = timerCanvas;
            ResultCanvas = resultCanvas;
            StartButton = startButton;
            RetryButton = retryButton;
            TitleButton = titleButton;
            ResultScoreText = resultScoreText;
            ScoreView = scoreView;
            TimerView = timerView;
            HoleViews = holeViews;
        }

        public GameObject TitleCanvas { get; }

        public GameObject GameplayCanvas { get; }

        public GameObject ScoreCanvas { get; }

        public GameObject TimerCanvas { get; }

        public GameObject ResultCanvas { get; }

        public Button StartButton { get; }

        public Button RetryButton { get; }

        public Button TitleButton { get; }

        public Text ResultScoreText { get; }

        public ScoreView ScoreView { get; }

        public TimerView TimerView { get; }

        public MoleHoleView[] HoleViews { get; }
    }
}
