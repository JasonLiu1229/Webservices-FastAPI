#!/bin/bash

# Function to start the webservice
start_webservice() {
    # Activate the virtual environment, one of the two commands will work (Linux/Windows)
    source venv/bin/activate || venv/Scripts/Activate
    # Install the required packages
    pip install -r requirements.txt
    # Start the webservice
    echo "Starting the webservice"
    python3 api_start.py &
    # Print the process id
    pid=$!
}

stop_webservice() {
    # Kill the process
    echo "Stopping the webservice"
    kill -9 $pid
    # wait for the process to terminate
    wait $pid
    # Deactivate the virtual environment
    deactivate
}

# Call the function
start_webservice

# Set a trap to stop the webservice
trap stop_webservice EXIT

# Wait for the webservice to stop
wait $pid

# Exit the script
exit 0
