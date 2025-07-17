# Spotify Playlog

## Overview
This project is an automated data pipeline intended to extract, load, and transform User's listening data from Spotify's API.
It collects raw data, stores, and transforms it into a structured format suitable for further analysis.
The pipeline pulls data about the songs you’ve listened to in the last 24 hours and loads this data into a destination such as a database.
A defined workflow orchestrates this process, allowing the pipeline to be scheduled to run daily, hourly, or at any desired frequency. Over time, you accumulate a history of your listening activity for deeper analysis.

## Project Structure
```
.
├── airflow
│   ├── dags
│   │   └── spotify_dag.py          # Main Airflow DAG definition
│   ├── airflow.sh                  # Script to start Airflow services
│   └── docker-compose.yaml         # Docker Compose setup for Airflow environment
├── src
│   ├── authentication
│   │   ├── auth.py                 # Authentication logic for Spotify API
│   │   └── tokens.py               # Token management
│   ├── data
│   │   ├── spotify_raw_data.json           # Raw data extracted from Spotify API
│   │   ├── spotify_transformed_data.csv    # Transformed data output file
│   │   └── token
│   │       └── refresh_token.json      # Stored refresh token for API access
│   ├── pipeline
│   │   ├── extract.py            # Data extraction from Spotify API
│   │   ├── load.py               # Loading data into storage/database
│   │   └── transform.py          # Data transformation logic
│   └── settings
│       ├── config.py             # Configuration settings for the project
│       └── logger.py             # Logger setup
├── .gitignore             # files that Git should ignore
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Python project metadata 
└── run.sh                 # Script to run the pipeline
```

## Technologies Used
- **Programming language:** 
  - Python 3.13.4
- **Database:** 
  - PostgreSQL 13.21
- **Python Libraries:**
  - numpy 2.3.0
  - pandas 2.3.0
  - psycopg2 2.9.10
  - urllib3 2.4.0
  - requests 2.32.3
  - SQLAlchemy 2.0.41
  - dotenv 1.1.0
- **Toolsets**
  - Docker 28.2.2
  - Apache Airflow 3.0.1
- **Data Sources:**
  - [Spotify API Documentation](https://developer.spotify.com/documentation/web-api)
