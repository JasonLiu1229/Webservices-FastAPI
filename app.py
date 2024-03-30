from fastapi import FastAPI

from routers import country, favorite

app = FastAPI(
    title="Country API",
    description="API to get country details and add to favorite list.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)


@app.get("/")
def read_root():
    return {'message': 'Check out the documentation at /docs'}


app.include_router(country.router)
app.include_router(favorite.router)
