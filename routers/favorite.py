from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def get_favorite():
    """
    Get a list of favorite items.
    :return: list of favorite items in json response
    """
    raise HTTPException(status_code=501, detail="Not implemented")


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
