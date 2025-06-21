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
    
    except Exception as e:
        print(f"Failed to create database engine: {e}")
        sys.exit(1)

def load_csv_to_table(data_path: Union[str, Path], table_name: str, engine: Engine) -> None:
    try:
        df = pd.read_csv(data_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully loaded into table '{table_name}'.")
    except Exception as e:
        print("Failed to load data into the database.")
        sys.exit(1)

def main() -> None:
    data_path = Config.TRANSFORMED_SPOTIFY_CSV_PATH
    table_name = "spotify_playlog"
    engine = get_database_engine()
    load_csv_to_table(data_path, table_name, engine)

if __name__ == "__main__":
    main()
