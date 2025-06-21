import base64
import json
import requests
from pathlib import Path
from settings.config import Config

def get_refresh_token(client_id: str, client_secret: str, redirect_uri: str, auth_code: str):
    url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    tokens = response.json()

    refresh_token = tokens.get("refresh_token")

    token_path = Path(__file__).parent.parent / "tmp" / "refresh_token.json"
    token_path.parent.mkdir(parents=True, exist_ok=True)
    with open(token_path, "w") as f:
        json.dump({"refresh_token": refresh_token}, f)

if __name__ == "__main__":
    get_refresh_token(client_id = Config.CLIENT_ID, 
                      client_secret = Config.CLIENT_SECRET, 
                      redirect_uri = Config.REDIRECT_URI, 
                      auth_code = Config.AUTH_CODE)