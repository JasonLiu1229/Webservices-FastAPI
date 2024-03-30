#!/bin/bash

# Function to call for API key using main.py
get_api_key() {
    # Read the API key from the user
    echo "Enter the API key"
    read api_key

    # Call the main.py script with the API key as an argument
    python3 main.py -key $api_key

    # Print the return code
    echo "Return code: $?"
}

# Function to test country using test.py
test_country_code() {
    echo "Testing country functions"

    python3 -c "import test; test.test_all_functions_country()"

    # Print the return code
    echo "Return code: $?"
}

# Function to test favorite using test.py
test_favorite() {
    exho "Testing favorite functions"

    python3 -c "import test; test.test_all_functions_favorite()"

    # Print the return code
    echo "Return code: $?"
}

# Function to test hottest country in South America using test.py
test_hottest_country() {
    python3 -c "import test; test.test_hottest_country_sa()"

    # Print the return code
    echo "Return code: $?"
}

# Call the function
get_api_key

# Call the test functions
test_country_code
test_favorite
test_hottest_country

# Exit the script
exit 0
