import json
import base64
import requests
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from settings.config import Config
from settings.logger import setup_logger

logger = setup_logger(Config.LOGGER_NAME, Config.LOGGER_PATH)

@dataclass
class TokenRequestPayload:
    """
    Payload containing headers and data for the Spotify refreshing access token request
    """
    headers: dict[str, str]
    data: dict[str, str]

@dataclass
class DataRequestPayload:
    """
    Payload containing headers for the Spotify 
    """
    headers: dict[str, str]

def load_refresh_token(token_path: str) -> str:
    """
    Loads the refresh token from a JSON file.

    Args:
        token_path (str): Path to the JSON file containing the refresh token.

    Returns:
        str: The refresh token extracted from the file.

    Raises:
        RuntimeError: If the file is not found or the 'refresh_token' key is missing.
    """
    try:
        logger.debug(f"Loading refresh token.")
        with open(token_path, encoding="utf-8") as file:
            refresh_token = json.load(file)["refresh_token"]
        logger.info("Refresh token loaded successfully.")
    except (FileNotFoundError, KeyError) as error:
        logger.error(f"Failed to load refresh token from {token_path}: {error}")
        raise

    return refresh_token

def build_token_request_payload(client_id: str, client_secret: str, refresh_token: str) -> TokenRequestPayload:
    """
    Builds the headers and data payload required to request a new Spotify access token using a refresh token.

    Args:
        client_id (str): The Spotify application's client ID.
        client_secret (str): The Spotify application's client secret.
        refresh_token (str): The previously obtained refresh token.

    Returns:
        TokenRequestPayload: A dataclass containing the headers and form data for the token refresh request.
    """
    logger.debug("Building token request payload.")
    try:
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers: dict[str, str] = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        logger.info("Token request payload successfully built.")
        return TokenRequestPayload(headers=headers, data=data)

    except Exception as error:
        logger.error(f"Failed to build token request payload: {error}", exc_info=True)
        raise

def refresh_access_token(payload: TokenRequestPayload) -> str:
    """
    Requests a new Spotify access token using the provided refresh token payload.

    Args:
        payload (TokenRequestPayload): Contains the headers and data needed for the token request.

    Returns:
        str: The new access token returned by Spotify.

    Raises:
        RuntimeError: If the HTTP request fails or returns a non-success status.
        ValueError: If the response does not contain an access token.
    """
    logger.info("Requesting new access token from Spotify.")
    url = "https://accounts.spotify.com/api/token"

    try:
        response = requests.post(url, headers = payload.headers, data = payload.data)
        response.raise_for_status()
        logger.info("Access token refreshed successfully.")
    except requests.RequestException as error:
        logger.error(f"Failed to refresh access token: {error}")
        raise
    
    new_access_token = response.json()["access_token"]
    if not new_access_token:
        logger.error("No access token found in Spotify's response.")
        raise

    return new_access_token

def build_data_request_payload(access_token: str) -> DataRequestPayload:
    """
    Constructs a payload containing the authorization headers for a Spotify API request.

    Args:
        access_token (str): A valid Spotify access token used to authorize API calls.

    Returns:
        DataRequestPayload: A dataclass containing the required HTTP headers.
    """
    logger.debug("Building data request payload.")

    try:
        headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}"
        }
    
        logger.info("Data request payload successfully built.")
        return DataRequestPayload(headers=headers)

    except Exception as error:
        logger.error(f"Failed to build data request payload: {error}", exc_info=True)
        raise

def get_recently_played_tracks(yesterday_unix_timestamp: str, payload: DataRequestPayload) -> Dict[str, Any]:
    """
    Retrieves the list of tracks recently played by the user after a specified Unix timestamp.

    Args:
        yesterday_unix_timestamp (str): A Unix timestamp (in milliseconds) indicating the earliest point in time 
                                        to fetch played tracks from.
        payload (DataRequestPayload): An object containing authorization headers.

    Returns:
        Dict[str, Any]: The JSON response from the Spotify API containing recently played tracks.

    Raises:
        RuntimeError: If the HTTP request fails or returns an error status.
    """
    logger.info("Fetching recently played tracks from Spotify.")
    url = f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={yesterday_unix_timestamp}"

    try:
        response = requests.get(url, headers = payload.headers)
        response.raise_for_status()
        logger.info("Recently played tracks fetched successfully.")
    except requests.HTTPError as http_error:
        logger.error(f"Spotify API returned an error: {http_error}")
        raise
    except requests.RequestException as request_error:
        logger.error(f"Request failed: {request_error}")
        raise
    
    return response.json()

def save_recently_played_tracks(data: Dict[str, Any], path: Path) -> None:
    """
    Saves the recently played tracks data to a JSON file.

    Args:
        data (Dict[str, Any]): Data to save (recently played tracks).
        path (Path): Destination file path.

    Raises:
        RuntimeError: If saving the file fails due to I/O errors.
    """
    logger.info(f"Saving recently played tracks.")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logger.info("Tracks saved successfully.")
    except (OSError, IOError) as error:
        logger.error(f"Failed to save refresh token to {path}: {error}")
        raise

def extract():
    logger.info("Starting Spotify ETL extract process.")
    try:
        refresh_token = load_refresh_token(Config.REFRESH_TOKEN_PATH)

        token_payload = build_token_request_payload(Config.CLIENT_ID, 
                                                    Config.CLIENT_SECRET, 
                                                    refresh_token)
        
        new_access_token = refresh_access_token(token_payload)

        data_payload = build_data_request_payload(new_access_token)
        spotify_data = get_recently_played_tracks(Config.unix_timestamp(), data_payload)
        
        save_recently_played_tracks(spotify_data, Config.SPOTIFY_RAW_DATA_PATH)
        logger.info("Spotify ETL extract process completed successfully.")
    except Exception as error:
        logger.critical(f"ETL extract failed: {error}.", exc_info=True)
        raise

if __name__ == "__main__":
    extract()