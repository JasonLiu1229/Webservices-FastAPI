from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_all_functions_country() -> None:
    """
    Test all the functions in the routers/country.py file.
    """
    pass


def test_all_functions_favorite() -> None:
    """
    Test all the functions in the routers/favorite.py file.
    """
    pass


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

    # Favorite the warmest country
    response = client.post(f"/favorite/{warmest_country[1]}")
    print(response.json())

    # Display the temperature forecast for the following four days
    response = client.get(f"/country/{warmest_country[1]}/forecast/{4}")
    print(response.json())
