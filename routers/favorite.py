from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    responses={404: {"description": "Not found"}}
)

FAVORITE_FILE = 'favorite.txt'

@router.get("")
async def get_favorite():
    """
    Get a list of favorite items.
    :return: list of favorite items in json response
    """
    try:
        with open(FAVORITE_FILE, 'r') as file:
            favorite_list = file.read().splitlines()
            # return list as json response
            return {"content": favorite_list}, 200
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Favorite list not found")


@router.post("/{country}")
async def add_favorite(country: str):
    """
    Add a country to favorite list.
    :param country: country in string
    :return: message in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{country}")
async def remove_favorite(country: str):
    """
    Remove a country from favorite list.
    :param country: country in string
    :return: message in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")
