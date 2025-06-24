import base64
import json
import requests
from pathlib import Path
from dataclasses import dataclass
from settings.config import Config

@dataclass
class TokenRequestPayload:
    """
    Payload containing headers and data for the Spotify token request.
    """
    headers: dict[str, str]
    data: dict[str, str]

@dataclass
class AuthResponse:
    """
    Data structure representing access and refresh tokens returned from Spotify.
    """
    access_token: str
    refresh_token: str

def build_token_request_payload(client_id: str, client_secret: str, auth_code: str, redirect_uri: str) -> TokenRequestPayload:
    """
    Build the payload required to request tokens from the Spotify API.

    Args:
        client_id (str): Spotify application's client ID.
        client_secret (str): Spotify application's client secret.
        auth_code (str): Authorization code obtained from the OAuth process.
        redirect_uri (str): Redirect URI used during the authorization.

    Returns:
        TokenRequestPayload: Object containing headers and form data for the request.
    """
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

def get_refresh_token(payload: TokenRequestPayload) -> AuthResponse:
    """
    Send a request to Spotify to exchange the authorization code for tokens.

    Args:
        payload (TokenRequestPayload): Headers and data required for the token request.

    Returns:
        AuthResponse: Object containing access and refresh tokens.

    Raises:
        RuntimeError: If the request fails or the response cannot be parsed.
        ValueError: If no refresh token is found in the response.
    """
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

    return AuthResponse(access_token = access_token, refresh_token = refresh_token)

def save_refresh_token(refresh_token: str, token_path: Path) -> None:
    """
    Save the refresh token to a JSON file at the specified path.

    Args:
        refresh_token (str): The refresh token to save.
        token_path (Path): The file path where the token will be saved.

    Raises:
        RuntimeError: If the file cannot be written to.
    """
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

    tokens: AuthResponse = get_refresh_token(payload)
    save_refresh_token(tokens.refresh_token, Config.REFRESH_TOKEN_PATH)