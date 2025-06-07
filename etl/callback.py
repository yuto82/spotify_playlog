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
            save_code_to_env(code)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful. You can close this tab.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h1>Error: No code received.</h1>")

def save_code_to_env(code_value):
    key = "CODE"
    path_dotenv = find_dotenv()
    with open(path_dotenv, "r") as f:
        lines = f.readlines()
    if any(line.startswith(f"{key}=") for line in lines):
        return 
    with open(path_dotenv, "a") as f:
        f.write(f"\n{key}={code_value}")

def authorize():

    webbrowser.open(
        f"https://accounts.spotify.com/authorize"
        f"?client_id={Config.CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={Config.REDIRECT_URI}"
        f"&scope=user-read-recently-played"
    )

    server = HTTPServer(("127.0.0.1", 8888), CallBackHandler)
    server.handle_request()

authorize()