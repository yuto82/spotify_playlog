import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict
from settings.config import Config

def load_data(raw_data_path: Path) -> dict[str, Any]:
    if not raw_data_path.exists():
        raise FileNotFoundError(f"Input file not found: {raw_data_path}")
    with open(raw_data_path, "r") as file:
        data = json.load(file)

    return data

def transform_track(data: dict[str, Any], transformed_data_path: Path) -> pd.DataFrame:
    items = data.get("items", [])
    if not items:
        raise ValueError("No items found in the input data")
    
    rows = [parse_track(item) for item in items]
    df = pd.DataFrame(rows)

    df = df[["artist_name", "artist_id", "song_name", "track_id", "duration_ms", "track_popularity", "played_at"]]
    df.columns = ["artist_name", "artist_id", "song_name", "track_id", "duration", "popularity", "played_at"]

    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").apply(
        lambda ms: f"{int(ms // 60000)}:{int((ms % 60000) // 1000):02}" if pd.notnull(ms) else None
    )

    df = df.drop_duplicates(subset="track_id", keep="first")
    df.to_csv(transformed_data_path, index=False)

    return df    

def parse_track(item: Dict[str, Any]) -> Dict[str, Any]:
    track = item.get("track", {})
    album = track.get("album", {})
    artist = album.get("artists", [{}])[0]

    return {
        "artist_name": artist.get("name"),
        "artist_id": artist.get("id"),
        "song_name": track.get("name"),
        "track_id": track.get("id"),
        "duration_ms": track.get("duration_ms"),
        "track_popularity": track.get("popularity"),
        "played_at": item.get("played_at")
    }

if __name__ == "__main__":
    data: dict[str, Any] = load_data(Config.SPOTIFY_RAW_DATA_PATH)
    transform_track(data, Config.SPOTIFY_TRANSFORMED_DATA_PATH)