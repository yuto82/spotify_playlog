import sys
import pandas as pd
from typing import Union
from pathlib import Path
from settings.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

def get_database_engine() -> Engine:
    """
    Creates and verifies a database engine connection using the configured database URL.

    Executes a simple test query to ensure the connection is valid.

    Returns:
        Engine: An SQLAlchemy Engine instance for interacting with the database.

    Raises:
        RuntimeError: If the engine creation or test query fails.
    """
    try:
        engine = create_engine(Config.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database engine created successfully.")
        return(engine)
    except Exception as error:
        raise RuntimeError(f"Failed to create database engine: {error}") from error

def load_data_to_database(data_path: Union[str, Path], table_name: str, engine: Engine) -> None:
    """
    Loads data into the specified database table.

    Reads the CSV file using pandas and writes the data into the database table using SQLAlchemy.
    Disposes the engine connection after successful loading.

    Args:
        data_path (Union[str, Path]): Path to the CSV file containing data to load.
        table_name (str): Name of the target database table.
        engine (Engine): SQLAlchemy Engine instance for database connection.

    Raises:
        RuntimeError: If reading the file or loading data into the database fails.
    """
    try:
        df = pd.read_csv(data_path)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        engine.dispose()
        print(f"Data successfully loaded into table '{table_name}'.")
    except Exception as error:
        raise RuntimeError(f"Failed to load data into the database: {error}") from error

def load():
    engine = get_database_engine()
    load_data_to_database(Config.SPOTIFY_TRANSFORMED_DATA_PATH, Config.TABLE_NAME, engine)

if __name__ == "__main__":
    load()