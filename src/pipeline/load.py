import sys
import pandas as pd
from typing import Union
from pathlib import Path
from settings.config import Config
from sqlalchemy.engine import Engine
from settings.logger import setup_logger
from sqlalchemy import create_engine, text

logger = setup_logger(Config.LOGGER_NAME, Config.LOGGER_PATH)

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
        logger.info(f"Creating database engine.")
        engine = create_engine(Config.DATABASE_URL)

        logger.debug("Testing database connection.")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database engine created and tested successfully.")
        return(engine)
    
    except Exception as error:
        logger.error(f"Failed to create database engine: {error}")
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
        logger.debug(f"Reading data from CSV file: {data_path}")
        df = pd.read_csv(data_path)

        logger.debug(f"Inserting data into table '{table_name}'.")
        df.to_sql(table_name, engine, if_exists='append', index=False)

        engine.dispose()
        logger.info(f"Data successfully loaded into table '{table_name}' and connection disposed.")

    except Exception as error:
        logger.error(f"Failed to load data into the database: {error}")
        raise RuntimeError(f"Failed to load data into the database: {error}") from error
    
def load():
    logger.info("Starting data load process.")
    try:
        engine = get_database_engine()
        load_data_to_database(Config.SPOTIFY_TRANSFORMED_DATA_PATH, Config.TABLE_NAME, engine)
        logger.info("Data load process completed successfully.")

    except Exception as error:
        logger.error(f"Data load process failed: {error}")
        raise

if __name__ == "__main__":
    load()