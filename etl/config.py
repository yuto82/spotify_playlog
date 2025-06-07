import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

path_dotenv = find_dotenv()
load_dotenv(path_dotenv)
class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")