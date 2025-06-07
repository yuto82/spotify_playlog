import json
from pathlib import Path
from components.config import Config
from components.auth import spotify_authorize, get_access_token, get_recent_tracks

def main():
    client_id = Config.CLIENT_ID
    client_secret = Config.CLIENT_SECRET
    redirect_uri = Config.REDIRECT_URI

    code = spotify_authorize(client_id, redirect_uri)
    access_token = get_access_token(client_id, client_secret, code, redirect_uri)
    spotify_data = get_recent_tracks(access_token)

    spotify_data_file = Path(__name__).parent.parent / "data" / "data.json"
    with open(spotify_data_file, "w") as file:
            json.dump(spotify_data, file, indent=4)

if __name__ == "__main__":
    main()