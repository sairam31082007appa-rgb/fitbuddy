import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = "FitBuddy"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Keep model names configurable through .env
GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-flash"
)

GEMINI_TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-2.5-flash"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)