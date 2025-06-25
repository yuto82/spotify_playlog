import os
import pytz
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

path_dotenv = find_dotenv()
load_dotenv(path_dotenv)

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    SCOPE = os.getenv("SCOPE")
    AUTH_CODE = os.getenv("AUTH_CODE")

    @staticmethod
    def get_unix_timestamp_yesterday() -> int:
        timezone = pytz.timezone("Europe/Warsaw")
        yesterday = datetime.now(timezone) - timedelta(days=1)
        return int(yesterday.timestamp()) * 1000

    DATABASE_URL = os.getenv("DATABASE_URL")
    
    SRC_DIR = Path(__file__).resolve().parent.parent

    REFRESH_TOKEN_PATH = SRC_DIR / "data" / "token" / "refresh_token.json"

    SPOTIFY_TRANSFORMED_DATA_PATH = SRC_DIR / "data" / "spotify_transformed_data.csv"
    SPOTIFY_RAW_DATA_PATH = SRC_DIR / "data" / "spotify_raw_data.json"

    
    