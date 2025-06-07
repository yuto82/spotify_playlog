import os
import base64
import requests
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

path_dotenv = find_dotenv()
load_dotenv(path_dotenv)

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# def access_token():
#     token_url = "https://accounts.spotify.com/api/token"

#     auth_header = base64.b64encode(f"{Config.CLIENT_ID}:{Config.CLIENT_SECRET}".encode()).decode()
#     headers = {
#         "Authorization": f"Basic {auth_header}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     data = {
#         "grant_type": "authorization_code",
#         "code": Config.CODE,
#         "redirect_uri": Config.REDIRECT_URI
#     }

#     response = requests.post(token_url, data=data, headers=headers)
#     tokens = response.json()
#     print("Access Token:", tokens.get("access_token"))
#     print("Refresh Token:", tokens.get("refresh_token"))
#     print("Expires In:", tokens.get("expires_in"))

