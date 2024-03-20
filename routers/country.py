from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(
    prefix="/country",
    tags=["country"],
    responses={404: {"description": "Not found"}}
)

COUNTRY_ERROR = "Country not found"


@router.get("")
async def get_country(continent: str):
    """
    Get a list of countries in a continent if continent is given.
    Else, get a list of all countries.
    :param continent: continent in string
    :return: list of countries in json response
    """
    continent = continent.lower()

    # make a request to rest countries to get a list of countries
    if continent:
        url = f"https://restcountries.com/v3.1/region/{continent}"
    else:
        url = "https://restcountries.com/v3.1/all"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Continent not found")
        countries = response.json()
        # filter out the country names
        country_list = [country['name']['common'] for country in countries]
        # return list of countries as json response
        return {"content": country_list}, 200


@router.get("/{country}")
async def get_country_detail(country: str):
    """
    Get details of a country.
    :param country: country in string
    :return: details of the country in json response
    """
    country = country.lower()

    # make a request to rest countries to get details of a country
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=COUNTRY_ERROR)
        country_detail = response.json()
        # return details of the country as json response
        return {"content": country_detail}, 200


@router.get("/{country}/temperature")
async def get_country_temperature(country: str):
    """
    Using the capital as the reference point, get the temperature of the country.

    :param country: country in string
    :return: temperature of the country in json response
    """
    country = country.lower()

    # make a request to rest countries to get the capital of a country
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=COUNTRY_ERROR)
        country_detail = response.json()
        capital = country_detail[0]['capital']

    # get capital latitude and longitude
    url = f"https://restcountries.com/v3.1/capital/{capital}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Capital not found")
        capital_detail = response.json()
        latlng = capital_detail[0]['latlng']
        latitude = latlng[0]
        longitude = latlng[1]

    # retrieve the keys from the keys.txt
    with open('keys.txt', 'r') as file:
        keys = file.read().splitlines()
        # retrieve the key from the keys
        key = keys[0]

    # make a request to openweathermap to get the temperature of the capital
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Temperature not found")
        temperature = response.json()
        # return temperature of the country as json response
        return {"content": temperature['main']['temp']}, 200


@router.get("/{country}/forecast/{day}")
async def get_country_forecast(country: str, day: int):
    """
    Get forecast of a country.
    :param country: country in string
    :param day: day in integer within a boundary of 1 to 5
    :return: forecast of the country in json response
    """
    country = country.lower()
    day = int(day)

    # forecast of country and make use of QuickChart to generate a chart
    # from data provided from openweathermap

    # make a request to rest countries to get the capital of a country

