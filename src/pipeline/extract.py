import json
import requests
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timedelta
from settings.config import Config
from authentication.access_token import refresh_access_token

def get_recently_played_tracks(access_token: str, yesterday_unix_timestamp: str) -> Dict[str, any]:
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def save_recently_played_tracks(data: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def extract_recently_played_tracks(client_id: str, client_secret: str, timezone: str) -> None:
    access_token: str = refresh_access_token(client_id, client_secret)

    yesterday = datetime.now(timezone) - timedelta(days=1)
    yesterday_unix_timestamp: int = int(yesterday.timestamp()) * 1000

    spotify_data: Dict[str, Any] = get_recently_played_tracks(access_token, yesterday_unix_timestamp)

    output_path = Path(__file__).parent.parent / "data" / "spotify_raw_data.json"

    save_recently_played_tracks(spotify_data, output_path)

if __name__ == "__main__":
    extract_recently_played_tracks(Config.CLIENT_ID,
                                   Config.CLIENT_SECRET,
                                   Config.CET)