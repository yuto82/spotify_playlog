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

