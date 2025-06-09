import json
import base64
import requests
from pathlib import Path

def get_access_token(client_id, client_secret, code, redirect_uri):
    url = "https://accounts.spotify.com/api/token"

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, data=data, headers=headers)
    tokens = response.json()
    
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    token_path = Path(__file__).parent.parent / "tmp" / "refresh_token.json"
    with open(token_path, "w") as file:
        json.dump({"refresh_token": refresh_token}, file)

    return access_token

def refresh_access_token(client_id, client_secret):
    token_path = Path(__file__).parent.parent / "tmp" / "refresh_token.json"
    with open(token_path) as file:
        refresh_token = json.load(file)["refresh_token"]

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

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    new_access_token = response.json().get("access_token")
    
    return new_access_token