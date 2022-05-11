from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from wiki.country import CountryDAL
from wiki.request_models import CountryClass

router = APIRouter(prefix="/v1/wiki")


@router.post("/continent/{continent_id}/country/", tags=["country"])
async def create_entry(request: Request, data: CountryClass, continent_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CountryDAL(session)
            try:
                id_ = await country_dal.create_entry(data, continent_id)
                if id_:
                    return JSONResponse(
                        status_code=200,
                        content={"id": id_, "message": "Added Continent Entry"},
                    )
                else:
                    return JSONResponse(status_code=422, content={"message": "Please check the Population"})
            except Exception:
                return JSONResponse(
                    status_code=422, content={"message": "Function Failed"},
                )


@router.get("/continent/{continent_id}/country", tags=["country"])
async def get_all_entries(request: Request, continent_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CountryDAL(session)
            try:
                return await country_dal.get_all_entries(continent_id)
            except Exception:
                return JSONResponse(
                    status_code=422, content={"message": "Function Failed"},
                )


@router.patch("/continent/{continent_id}/country/{country_id}", tags=["country"])
async def update_entry(
    request: Request,
    data: CountryClass,
    continent_id: int,
    country_id: int,
):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CountryDAL(session)
            try:
                await country_dal.update_entry(data, continent_id, country_id)
                return JSONResponse(
                    status_code=200, content={"message": "Updated Country Entry"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422, content={"message": "Function Failed"},
                )


@router.delete("/continent/{continent_id}/country/{country_id}", tags=["country"])
async def delete_entry(request: Request, country_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CountryDAL(session)
            try:
                await country_dal.delete_entry(country_id)
                return JSONResponse(
                    status_code=200, content={"message": "Continent Entry Deleted"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422, content={"message": "Function Failed"},
                )
