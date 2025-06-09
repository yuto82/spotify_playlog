import json
import requests
from pathlib import Path
from settings.config import Config
from services.auth import authorization
from services.token import get_access_token

def main():
    client_id = Config.CLIENT_ID
    client_secret = Config.CLIENT_SECRET
    redirect_uri = Config.REDIRECT_URI
    scope = Config.SCOPE

    auth_code = authorization(client_id, redirect_uri, scope)
    access_token = get_access_token(client_id, client_secret, auth_code, redirect_uri)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    spotify_data = response.json()

    spotify_data_file = Path(__file__).parent / "tmp" / "data.json"

    with open(spotify_data_file, "w") as file:
            json.dump(spotify_data, file, indent=4)

if __name__ == "__main__":
    main()