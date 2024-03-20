from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    responses={404: {"description": "Not found"}}
)

FAVORITES_FILE = 'favorites.txt'
FILE_ERROR = "Favorite list not found"


@router.get("")
async def get_favorite():
    """
    Get a list of favorite items.
    :return: list of favorite items in json response
    """
    try:
        with open(FAVORITES_FILE, 'r') as file:
            favorite_list = file.read().splitlines()
            # return list as json response
            return {"content": favorite_list}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=FILE_ERROR)


@router.post("/{country}")
async def add_favorite(country: str):
    """
    Add a country to favorite list.
    :param country: country in string
    :return: message in json response
    """
    country = country.lower()

    # make a request to rest countries to check if country exists
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Country not found")
    # add country to a favorite list
    try:
        # check if it already exists in the file
        with open(FAVORITES_FILE, 'r') as file:
            favorite_list = file.read().splitlines()
            if country in favorite_list:
                raise HTTPException(status_code=400, detail="Country already in favorite list")
        with open(FAVORITES_FILE, 'a') as file:
            file.write(country + '\n')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=FILE_ERROR)
    return {"message": f"{country} added to favorite list"}


@router.delete("/{country}")
async def remove_favorite(country: str):
    """
    Remove a country from a favorite list.
    :param country: country in string
    :return: message in json response
    """
    try:
        with open(FAVORITES_FILE, 'r') as file:
            favorite_list = file.read().splitlines()
        if country not in favorite_list:
            raise HTTPException(status_code=404, detail="Country not found in favorite list")
        with open(FAVORITES_FILE, 'w') as file:
            for item in favorite_list:
                if item != country:
                    file.write(item + '\n')
        return {"message": f"{country} removed from favorite list"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=FILE_ERROR)
