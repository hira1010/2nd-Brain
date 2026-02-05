
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Configuration
VIDU_API_KEY = os.getenv("VIDU_API_KEY")
VIDU_API_URL = "https://api.vidu.studio/v1/generate" # Hypothetical endpoint, to be adjusted based on actual API docs

# Default Generation Settings
DEFAULT_RESOLUTION = "1080p"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_DURATION = 4 # seconds

if not VIDU_API_KEY:
    print("Warning: VIDU_API_KEY is not set. Please set it in .env or environment variables.")
