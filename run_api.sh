#!/bin/bash

# Function to start the webservice
start_webservice() {
    # Activate the virtual environment, one of the two commands will work (Linux/Windows)
    source venv/bin/activate || source venv/Scripts/activate
    # Install the required packages
    pip install -r requirements.txt
    # Start the webservice
    python3 api_start.py
}

# Call the function
start_webservice