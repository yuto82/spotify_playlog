import base64
import json
import requests
from pathlib import Path
from dataclasses import dataclass
from settings.config import Config

@dataclass
class TokenRequestPayload:
    headers: dict[str, str]
    data: dict[str, str]

def build_token_request_payload(client_id: str, client_secret: str, auth_code: str, redirect_uri: str) -> TokenRequestPayload:
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers: dict[str, str] = {
        "Authorization": f"Basic {auth_header}", 
        "Content-Type": "application/x-www-form-urlencoded"
        }

    data: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
        }
    
    return TokenRequestPayload(headers = headers, data = data)

def get_refresh_token(payload: TokenRequestPayload) -> tuple[str, str]:
    url = "https://accounts.spotify.com/api/token"

    try:
        response = requests.post(url, headers = payload.headers, data = payload.data)
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError("Failed to get token from Spotify.") from error

    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise ValueError("No refresh token found in the response from Spotify.")

    return(access_token, refresh_token)

def save_refresh_token(refresh_token: str, token_path: Path) -> None:
    try:
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as file:
            json.dump({"refresh_token": refresh_token}, file)    
        print(f"Refresh token saved to {token_path}")
    except (OSError, IOError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Failed to save refresh token to {token_path}") from error

if __name__ == "__main__":
    payload: TokenRequestPayload = build_token_request_payload(client_id = Config.CLIENT_ID, 
                                                               client_secret = Config.CLIENT_SECRET, 
                                                               auth_code = Config.AUTH_CODE, 
                                                               redirect_uri = Config.REDIRECT_URI)

    access_token, refresh_token = get_refresh_token(payload)
    save_refresh_token(refresh_token, token_path = Config.REFRESH_TOKEN_PATH)