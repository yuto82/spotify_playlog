import json
import pandas as pd
from pathlib import Path

def transform_data() -> None:
    file_path = Path(__file__).parent.parent / "tmp" / "data" / "spotify_data.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(file_path, "r") as file:
        data = json.load(file)

    items = data.get("items", [])

    transformed_data = []

    for item in items:
        track = item.get("track", {})
        album = track.get("album", {})
        artist = album.get("artists", [{}])[0]

        transformed_data.append({
            "artist_name": artist.get("name"),
            "artist_id": artist.get("id"),
            "song_name": track.get("name"),
            "track_id": track.get("id"),
            "duration_ms": track.get("duration_ms"),
            "track_popularity": track.get("popularity"),
            "played_at": item.get("played_at")
        })
            
    df = pd.DataFrame(transformed_data)
    df = df[["artist_name", "artist_id", "song_name", "track_id", "duration_ms", "track_popularity", "played_at"]]
    df.columns = ["artist_name", "artist_id", "song_name", "track_id", "duration", "popularity", "played_at"]

    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce")
    df["played_at"] = df["played_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df["duration"] = df["duration"].apply(
        lambda ms: f"{int(ms // 60000)}:{int((ms % 60000) // 1000):02}" if pd.notnull(ms) else None
        )

    df = df.drop_duplicates(subset="track_id", keep="first")

    output_path = Path(__file__).parent.parent / "tmp" / "data" / "spotify_transformed.csv"
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    transform_data()