from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/country",
    tags=["country"],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def get_country(continent: str):
    """
    Get a list of countries in a continent if continent is given.
    Else, get a list of all countries.
    :param continent: continent in string
    :return: list of countries in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{country}")
async def get_country_detail(country: str):
    """
    Get details of a country.
    :param country: country in string
    :return: details of the country in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{country}/temperature")
async def get_country_temperature(country: str):
    """
    Get temperature of a country.
    :param country: country in string
    :return: temperature of the country in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{country}/forecast/{day}")
async def get_country_forecast(country: str, day: int):
    """
    Get forecast of a country.
    :param country: country in string
    :param day: day in integer within a boundary of 1 to 5
    :return: forecast of the country in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")
