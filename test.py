from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_all_functions_country() -> None:
    """
    Test all the functions in the routers/country.py file.
    """
    # Test the get_country function with a continent parameter
    print(client.get("/country?continent=asia").json())

    print('-----------------------------------')

    # Test the get_country function without a continent parameter
    print(client.get("/country").json())

    print('-----------------------------------')

    # Test the get_country_detail function with a country parameter
    print(client.get("/country/india").json())

    print('-----------------------------------')

    # Test the get_country_temperature function with a country parameter
    print(client.get("/country/india/temperature").json())

    print('-----------------------------------')

    # Test the get_country_forecast function with a country and days parameter
    print('Forecast for the next four days for India saved in forecast_india_4.png')
    response = client.get("/country/india/forecast/4")
    with open('forecast_india_4.png', 'wb') as file:
        file.write(response.content)

    print('-----------------------------------')

    # Test the get_country_forecast function with a country and days parameter
    print('Forecast for the next day for India saved in forecast_india_1.png')
    response = client.get("/country/india/forecast/1")
    with open('forecast_india_1.png', 'wb') as file:
        file.write(response.content)

    print('-----------------------------------')


def test_all_functions_favorite() -> None:
    """
    Test all the functions in the routers/favorite.py file.
    """
    # Test the get_favorite function
    print(client.get("/favorite").json())

    print('-----------------------------------')

    # Test the add_favorite function with a country parameter
    print(client.post("/favorite/india").json())

    print('-----------------------------------')

    # Test the get_favorite function
    print(client.get("/favorite").json())

    print('-----------------------------------')

    # Test the remove_favorite function with a country parameter
    print(client.delete("/favorite/india").json())

    print('-----------------------------------')

    # Test the get_favorite function
    print(client.get("/favorite").json())

    print('-----------------------------------')


def test_hottest_country_sa() -> None:
    """
    Test the hottest country in South America and answer the query of which country in South America is currently the
    warmest.
    You should favorite that country and display a line graph containing the temperature forecast for the
    following four days.
    """
    response = client.get("/country?continent=south%20america")
    list_of_temp = []
    for country in response.json()["List of countries"]:
        list_of_temp.append((client.get(f"/country/{country}/temperature").json()["Temperature"], country))
    warmest_country = max(list_of_temp)
    print(warmest_country[1])

    print('-----------------------------------')

    # Display the favorite list
    response = client.get("/favorite")
    print(response.json())

    print('-----------------------------------')

    # Favorite the warmest country
    response = client.post(f"/favorite/{warmest_country[1]}")
    print(response.json())

    print('-----------------------------------')

    # Display the favorite list
    response = client.get("/favorite")
    print(response.json())

    print('-----------------------------------')

    # Display the temperature forecast for the following four days
    response = client.get(f"/country/{warmest_country[1]}/forecast/{4}")
    # write image to a file
    print(f'Forecast for the next 4 days for {warmest_country[1]} saved in forecast_{warmest_country[1]}_4.png')
    with open(f'forecast_{warmest_country[1]}_4.png', 'wb') as file:
        file.write(response.content)

    print('-----------------------------------')
