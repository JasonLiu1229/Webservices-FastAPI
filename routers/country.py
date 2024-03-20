from fastapi import APIRouter, HTTPException
import httpx
import datetime
import time

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
        return {"content": country_list}


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
        # retrieve longitude and latitude, population and area of capital
        country_detail_filtered = {
            "capital": country_detail[0]['capital'],
            "latitude": country_detail[0]['capitalInfo']['latlng'][0],
            "longitude": country_detail[0]['capitalInfo']['latlng'][1],
            "population": country_detail[0]['population'],
            "area": country_detail[0]['area']
        }
        return {"content": country_detail_filtered}


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
        latitude = country_detail[0]['capitalInfo']['latlng'][0]
        longitude = country_detail[0]['capitalInfo']['latlng'][1]

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
    Three-hourly based on the current date.
    :param country: country in string
    :param day: day in integer within a boundary of 1 to 5
    :return: forecast of the country in json response
    """
    if day < 1 or day > 5:
        raise HTTPException(status_code=400, detail="Day should be within 1 to 5")

    country = country.lower()
    day = int(day)

    # forecast of country and make use of QuickChart to generate a chart
    # from data provided from openweathermap

    # make a request to rest countries to get the capital of a country
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=COUNTRY_ERROR)
        country_detail = response.json()
        latitude = country_detail[0]['latlng'][0]
        longitude = country_detail[0]['latlng'][1]

    # retrieve the keys from the keys.txt
    with open('keys.txt', 'r') as file:
        keys = file.read().splitlines()
        # retrieve the key from the keys
        key = keys[0]

    current_date = datetime.datetime.now()

    saved_data = []

    # make a request to openweathermap to get the forecast of the capital
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={latitude}"
        f"&lon={longitude}"
        f"&appid={key}"
        f"&units=metric"
        f"&cnt={day * 8}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Forecast not found")
        forecast = response.json()
        # return forecast of the country as json response

    # make a request to QuickChart to generate a chart
    url = "https://quickchart.io/chart/create"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=convert_data_to_chartJS(forecast.get('list')))
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Chart not found")
        chart = response.json()
        # return chart of the forecast as json response
        return {"content": chart['url']}, 200




def convert_data_to_chartJS(data: list):
    """
    Convert a list of data to chartJS format supported by QuickChart

    :param data: List of data
    :return: chartJS format
    """
    labels = []
    temperatures = []
    chart_data = {}
    for item in data:
        # convert date to human readable format
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['dt']))
        labels.append(date)
        temperatures.append(item.get('main').get('temp'))
    chart_data['labels'] = labels
    chart_data['datasets'] = [
        {
            "label": "Temperature",
            "data": temperatures,
            "fill": False,
            "borderColor": "rgb(75, 192, 192)",
            "lineTension": 0.1
        }
    ]
    return chart_data
