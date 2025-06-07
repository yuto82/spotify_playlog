import json
from callback_handler import spotify_authorize, access_token, get_recent_tracks

def main():
    code = spotify_authorize()

    acess_token = access_token(code)
    
    spotify_data = get_recent_tracks(acess_token)
    

    spotify_file = "spotify_data.json"
    with open(spotify_file, "w") as file:
            json.dump(spotify_data, file, indent=4)

if __name__ == "__main__":
    main()