import os
import requests
import base64
import webbrowser
from pathlib import Path
from dotenv import load_dotenv

path_dotenv = Path(__file__).parent.parent / ".env"
load_dotenv(path_dotenv)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
CODE = os.getenv("CODE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def authorize():
    url = (
        "https://accounts.spotify.com/authorize"
        "?client_id=" + CLIENT_ID +
        "&response_type=code" +
        "&redirect_uri=" + REDIRECT_URI +
        "&scope=" + "user-read-recently-played"
    )

    webbrowser.open(url)

def access_token():
    token_url = "https://accounts.spotify.com/api/token"

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": CODE,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()
    print("Access Token:", tokens.get("access_token"))
    print("Refresh Token:", tokens.get("refresh_token"))
    print("Expires In:", tokens.get("expires_in"))


def get_recent_tracks(access_token=ACCESS_TOKEN):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data["items"])