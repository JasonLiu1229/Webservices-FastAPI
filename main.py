import argparse


parser = argparse.ArgumentParser(description="Country API")

parser.add_argument("-key", "--openweathermap-api-key",
                    required=True,
                    help="OpenWeatherMap API key",
                    type=str
                    )

# write keys to a file
with open('keys.txt', 'w') as file:
    file.write(parser.parse_args().openweathermap_api_key)
