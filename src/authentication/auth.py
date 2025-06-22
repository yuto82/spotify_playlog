import webbrowser
from urllib.parse import urlencode
from settings.config import Config

def build_authentication_url(client_id: str, redirect_uri: str, scope: str) -> str:
    """
    Builds Spotify OAuth 2.0 authorization URL.

    Args:
        client_id (str): Spotify application client ID.
        redirect_uri (str): URI to redirect to after authorization.
        scope (str): A space-separated list of Spotify access scopes.

    Returns:
        str: Fully constructed Spotify authorization URL with query parameters.
    """
    query = urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    })

    return (f"https://accounts.spotify.com/authorize?{query}")


def open_authentication_url(url: str) -> None:
    """
    Opens given URL in the default web browser.

    Args:
        url (str): The URL to be opened.
    """
    webbrowser.open(url)

if __name__ == "__main__":
    url: str = build_authentication_url(Config.CLIENT_ID, Config.REDIRECT_URI, Config.SCOPE)
    open_authentication_url(url)