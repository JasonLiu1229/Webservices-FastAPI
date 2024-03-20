import uvicorn
import argparse

from app import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Country API")

    parser.add_argument("-owm-key", "--openweathermap-api-key",
                        required=True,
                        help="OpenWeatherMap API key",
                        type=str
                        )

    parser.add_argument("-rc-key",
                        "--restfull-countries-api-key",
                        required=True,
                        help="Restful Countries API key",
                        )

    # write keys to a file
    with open('keys.txt', 'w') as file:
        file.write(f"OWM_KEY={parser.openweathermap_api_key}\n")
        file.write(f"RC_KEY={parser.restfull_countries_api_key}\n")

    uvicorn.run(app, port=8000)
