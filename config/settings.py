import os

from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY or not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Missing necessary API keys in environment variables.")
