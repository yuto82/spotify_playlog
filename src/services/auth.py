import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

auth_data = {}
class CallBackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_data['code'] = parse_qs(urlparse(self.path).query).get("code", [None])[0]

def authorization(client_id, redirect_uri, scope):
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
    )

    webbrowser.open(url)

    server_address = (urlparse(redirect_uri).hostname, urlparse(redirect_uri).port)
    
    with HTTPServer(server_address, CallBackHandler) as server:
        server.handle_request()

    return auth_data.get('code')