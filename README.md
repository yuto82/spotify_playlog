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

## Pipeline Breakdown
This project implements an ETL (Extract, Transform, Load) pipeline for collecting, transforming, and storing User's listening data from the Spotify API. The pipeline includes the following stages:

### Task 1: Initial authorization
- **Modules involved:** `auth.py`
- **Objective:** Initiate the Spotify OAuth 2.0 flow to obtain User's authorization for accessing listening data.
- **Main steps:**
  - **Build Authorization URL**: 
  <br> The function `build_authentication_url()` constructs a Spotify authorization URL using client credentials, requested scopes, and a redirect URI.
  - **User Consent Flow:**
  <br> The constructed URL is opened in the default web browser using the `open_authentication_url()` function, prompting the user to log in and approve access.
  - **Manual Step**:
  <br> This authorization code can be manually copied from the redirect URL (e.g., `...?code=...`) and used in the next step of the pipeline to request tokens.
- **Expected Output:**
  - A one-time authorization code, valid for 10 minutes.
  - Though not used directly in the pipeline, it is essential during initial setup to obtain long-term refresh tokens.

### Task 2: Token Request
- **Modules involved:** `token.py`
- **Objective:** Exchange the authorization code for an access token and a refresh token, then persist the refresh token for future use.
- **Main steps:**
  - **Build Token Request Payload:**
  <br> The `build_tokens_request_payload()` function prepares the required headers and data, including client credentials, redirect URI, and authorization code, for the token exchange request.
  - **Exchange Code for Tokens:**
  <br> Here, the function `get_refresh_token()` sends a POST request to Spotify’s token endpoint and parses the response to retrieve access and refresh token.
  - **Store Token:**
  <br> The `save_refresh_token()` function saves the refresh token to a local JSON file for reuse in future sessions.
- **Expected Output:**
  - A valid `access token` for immediate use and a `refresh_token` to refresh it later.
  - The refresh token is stored securely in the filesystem, enabling long-term API access without repeating manual authorization.

### Task 3: Extraction
- **Modules involved:** `extract.py`
- **Objective:** Extract recently played track data from the Spotify Web API using a valid access token.
- **Main steps:**
  - **Load Refresh Token:**
  <br> Function `load_refresh_token()` reads the previously saved refresh token from local storage.
  - **Request New Access Token:**
  <br> These functions `build_token_request_payload()` and `refresh_access_token()` are used to build the token payload and obtain a new short-lived access token via the Spotify API.
  - **Build Data Request Headers:**
  <br> `build_data_request_payload()` prepares authorization headers using the new access token.
  - **Request User's Playback Data:**
  <br> The `get_recently_played_tracks()` function queries the `/v1/me/player/recently-played` endpoint with a Unix timestamp filter, retrieving up to 50 recent tracks.
  - **Persist Raw Data:**
  <br> The result is saved locally using `save_recently_played_tracks()` as a raw JSON file for downstream processing.
- **Expected Output:**
  - A JSON file containing track metadata and playback history after the defined timestamp.
  - Includes information such as track name, artist, album, playback timestamp, and additional metadata from Spotify.