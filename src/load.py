import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from components.settings.config import Config

def create_database_engine():
    try:
        engine = create_engine(Config.DATABASE_URL)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database engine created successfully.")
        return(engine)
    
    except Exception as e:
        print(f"Failed to create database engine: {e}")
        sys.exit(1)

def load_data(file, table_name):
    engine = create_database_engine()
    
    try:
        data = pd.read_csv(file)
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Data successfully loaded into the database.")

    except Exception as e:
        print(f"Failed to load data into the database: {e}")
        sys.exit(1)

def main():
    file = Path(__file__).parent.parent / "tmp" / "data" / "spotify_transformed.csv"

    table_name = "spotify_playlog"

    load_data(file, table_name)

if __name__ == "__main__":
    main()