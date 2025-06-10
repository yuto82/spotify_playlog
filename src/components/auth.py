import webbrowser
from settings.config import Config

def spotify_auth_url(client_id: str, redirect_uri: str, scope: str):
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
    )

    print(url)
    webbrowser.open(url)

if __name__ == "__main__":
    spotify_auth_url(Config.CLIENT_ID,
                     Config.REDIRECT_URI,
                     Config.SCOPE)
