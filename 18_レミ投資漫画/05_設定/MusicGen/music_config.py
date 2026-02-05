
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ACE_STEP_REPO_PATH = os.path.join(BASE_DIR, "ACE-Step-1.5")
MODELS_DIR = os.path.join(ACE_STEP_REPO_PATH, "models") # Default location, might vary based on acestep logic

# Generation Defaults
DEFAULT_MODEL = "ACE-Step/Ace-Step1.5"
DEFAULT_DIT_MODEL = "acestep-v15-turbo"
DEFAULT_LM_MODEL = "acestep-5Hz-lm-1.7B"

DEFAULT_DURATION = 30  # seconds
DEFAULT_BPM = 120

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
