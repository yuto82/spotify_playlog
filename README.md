# Spotify Playlog

## Overview
This project is an automated data pipeline intended to extract, load, and transform User's listening data from Spotify's API.
It collects raw data, stores, and transforms it into a structured format suitable for further analysis.
The pipeline pulls data about the songs you’ve listened to in the last 24 hours and loads this data into a destination such as a database.
A defined workflow orchestrates this process, allowing the pipeline to be scheduled to run daily, hourly, or at any desired frequency. Over time, you accumulate a history of your listening activity for deeper analysis.