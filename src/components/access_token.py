import base64
import json
import requests
from pathlib import Path

def refresh_access_token(client_id, client_secret):
    token_path = Path(__file__).parent.parent / "tmp" / "refresh_token.json"
    with open(token_path) as f:
        refresh_token = json.load(f)["refresh_token"]

    url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    
    access_token = response.json()["access_token"]

    return access_token
