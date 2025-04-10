from dotenv import load_dotenv
import os
from . import common

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not ALPHA_VANTAGE_API_KEY:
	raise ValueError("ALPHA_VANTAGE_API_KEY not found. Please set it in your environment variables.")
