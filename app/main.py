import uvicorn
from fastapi import FastAPI

from app import datastore
from routes import city_router
from routes import continent_router
from routes import country_router
from wiki.models import Base

# Create fastAPI app
app = FastAPI()

# Attach db modules to app
app.datastore = datastore  # type: ignore
app.include_router(continent_router.router)
app.include_router(country_router.router)
app.include_router(city_router.router)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Call startup functions
    """
    # Table stuff
    async_engine = await app.datastore.get_datastore("engine")
    async with async_engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all)
        await engine.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(app, port=1111, host="127.0.0.1")
