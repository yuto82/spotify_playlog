#!/bin/bash
PYTHON=python3

# Check if the virtual environment exists
echo "Checking the virtual environment..."
if [ -d "venv" ]; then
  echo "Virtual environment found."
  # Activate the virtual environment
  source venv/bin/activate
  echo "Activated."
else
  # If the venv folder is missing, exit with error
  echo "Virtual environment not found. Execution stopped."
  exit 1
fi

echo "extract.py running..."
# Run extract.py to get data from APIs
$PYTHON src/pipeline/extract.py

# Check for errors after running extract.py
if [ $? -ne 0 ]; then
  echo "extract.py failed. Execution stopped."
  exit 1
fi

echo "transform.py running..."
# Run transform.py to clean and convert the data
$PYTHON src/pipeline/transform.py

# Check for errors after running transform.py
if [ $? -ne 0 ]; then
  echo "transform.py failed. Execution stopped."
  exit 1
fi

echo "load.py running..."
# Run load.py to load the data into the database
$PYTHON src/pipeline/load.py

# Check for errors after running load.py
if [ $? -ne 0 ]; then
  echo "load.py failed. Execution stopped."
  exit 1
fi

echo "All steps completed successfully."