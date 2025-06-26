import sys
import pandas as pd
from typing import Union
from pathlib import Path
from settings.config import Config
from sqlalchemy import create_engine, text, Engine

def get_database_engine() -> Engine:
    try:
        engine = create_engine(Config.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database engine created successfully.")
        return(engine)
    except Exception as error:
        raise RuntimeError(f"Failed to create database engine: {error}") from error

def load_csv_to_table(data_path: Union[str, Path], table_name: str, engine: Engine) -> None:
    try:
        df = pd.read_csv(data_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully loaded into table '{table_name}'.")
    except Exception as error:
        raise RuntimeError(f"Failed to load data into the database: {error}") from error

if __name__ == "__main__":
    engine = get_database_engine()
    load_csv_to_table(Config.SPOTIFY_TRANSFORMED_DATA_PATH, Config.TABLE_NAME, engine)