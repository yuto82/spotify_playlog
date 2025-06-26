import json
import pandas as pd
from pathlib import Path
from typing import Any, Dict
from settings.config import Config

def load_data(raw_data_path: Path) -> dict[str, Any]:
    """
    Loads JSON data from the specified file path.

    Args:
        raw_data_path (Path): Path to the JSON file to load.

    Returns:
        dict[str, Any]: the JSON data as a dictionary.

    Raises:
        FileNotFoundError: If the file at raw_data_path does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    if not raw_data_path.exists():
        raise FileNotFoundError(f"Input file not found: {raw_data_path}")
    
    try:
        with open(raw_data_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON file: {raw_data_path}") from error

    return data

def parse_track(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses a single track item from Spotify's recently played data structure
    and extracts relevant track and artist information.

    Args:
        item (Dict[str, Any]): A dictionary representing a single track play event,
                               typically one entry from the "items" list in the Spotify API response.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - artist_name (str | None): Comma-separated artist names.
            - artist_id (str | None): Comma-separated artist IDs.
            - song_name (str | None): Name of the track.
            - track_id (str | None): Spotify ID of the track.
            - duration_ms (int | None): Duration of the track in milliseconds.
            - track_popularity (int | None): Popularity score of the track.
            - played_at (str | None): ISO timestamp when the track was played.
    """
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

def transform_track(data: dict[str, Any], transformed_data_path: Path) -> pd.DataFrame:
    """
    Transforms raw Spotify recently played track data into a cleaned pandas DataFrame,
    formats fields, removes duplicates, and saves the result as a CSV file.

    Args:
        data (dict[str, Any]): Raw JSON data from Spotify API containing recently played tracks.
        transformed_data_path (Path): Path to save the transformed CSV data.

    Raises:
        ValueError: If no 'items' are found in the input data.

    Returns:
        pd.DataFrame: The cleaned and transformed DataFrame.
    """
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

if __name__ == "__main__":
    data: dict[str, Any] = load_data(Config.SPOTIFY_RAW_DATA_PATH)
    transform_track(data, Config.SPOTIFY_TRANSFORMED_DATA_PATH)