import base64
import json
import requests
from pathlib import Path
from settings.config import Config

def build_auth_headers(client_id: str, client_secret: str) -> dict[str, str]:
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    return {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"}

def build_token_request_data(auth_code: str, redirect_uri: str) -> dict[str, str]:

    return {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri}

def save_refresh_token(token: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump({"refresh_token": token}, f)

def get_refresh_token(client_id: str, client_secret: str, redirect_uri: str, auth_code: str, token_path: Path) -> None:
    url = "https://accounts.spotify.com/api/token"

    headers = build_auth_headers(client_id, client_secret)
    data = build_token_request_data(auth_code, redirect_uri)

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError("Failed to get token from Spotify.") from e

    tokens = response.json()
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise ValueError("No refresh token found in the response from Spotify.")

    save_refresh_token(refresh_token, token_path)
    print(f"Refresh token saved to {token_path}")

if __name__ == "__main__":
    get_refresh_token(client_id = Config.CLIENT_ID, 
                      client_secret = Config.CLIENT_SECRET, 
                      redirect_uri = Config.REDIRECT_URI, 
                      auth_code = Config.AUTH_CODE,
                      token_path = Config.REFRESH_TOKEN_PATH)