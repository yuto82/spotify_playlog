import base64
import requests
import webbrowser
from config import Config
from dotenv import find_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class CallBackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        code = params.get("code", [None])[0]
        if code:
            self.server.authorization_code = code
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful. You can close this tab.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h1>Error: No code received.</h1>")

def spotify_authorize():
    webbrowser.open(
        f"https://accounts.spotify.com/authorize"
        f"?client_id={Config.CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={Config.REDIRECT_URI}"
        f"&scope=user-read-recently-played"
    )

    server = HTTPServer(("127.0.0.1", 8888), CallBackHandler)
    server.authorization_code = None
    server.handle_request()
    return server.authorization_code

def access_token(code):
    token_url = "https://accounts.spotify.com/api/token"

    auth_header = base64.b64encode(f"{Config.CLIENT_ID}:{Config.CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.REDIRECT_URI
    }

    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expired = tokens.get("expires_in")

    return access_token

def get_recent_tracks(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data
