import json
import requests
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timedelta
from components.settings.config import Config
from components.access_token import refresh_access_token

def get_recently_played_tracks(access_token: str, yesterday_unix_timestamp: str) -> Dict[str, any]: 
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



# def extract(client_id: str, client_secret: str, timezone: str):
#     refreshed_access_token = refresh_access_token(client_id, client_secret)
    
#     headers = {
#         "Authorization": f"Bearer {refreshed_access_token}"
#     }

#     yesterday_timestamp = datetime.now(timezone) - timedelta(days=1)
#     yesterday_unix_timestamp = int(yesterday_timestamp.timestamp()) * 1000

#     url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}"

#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     if response.status_code == 200:
#         spotify_data = response.json()
#     else:
#         print(f'Failed to get recently played tracks. Response: {response.json()}')

#     spotify_data_file = Path(__file__).parent.parent / "tmp" / "data" / "spotify_data.json"

#     with open(spotify_data_file, "w") as file:
#             json.dump(spotify_data, file, indent=4)

# if __name__ == "__main__":
#     extract(Config.CLIENT_ID,
#             Config.CLIENT_SECRET,
#             Config.CET)