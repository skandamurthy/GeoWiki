from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from wiki.city import CityDAL
from wiki.request_models import CityClass

router = APIRouter(prefix="/v1/wiki")


@router.post(path="/country/{country_id}/city/", tags=["city"])
async def create_entry(request: Request, data: CityClass, country_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CityDAL(session)
            try:
                id_ = await country_dal.create_entry(data, country_id)
                if id_:
                    return JSONResponse(
                        status_code=200,
                        content={"id": id_, "message": "Added City Entry"},
                    )
                else:
                    return JSONResponse(
                        status_code=422,
                        content={"message": "Please check the Population"},
                    )
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Data entry Failed"},
                )


@router.get(path="/country/{country_id}/city", tags=["city"])
async def get_all_entries(request: Request, country_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CityDAL(session)
            try:
                await country_dal.get_all_entries(country_id)
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )


@router.patch(path="/country/{country_id}/city/{city_id}", tags=["city"])
async def update_entry(
    request: Request,
    data: CityClass,
    country_id: int,
    city_id: int,
):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CityDAL(session)
            try:
                await country_dal.update_entry(
                    data=data,
                    country_id=country_id,
                    city_id=city_id,
                )
                return JSONResponse(
                    status_code=200,
                    content={"message": "Updated City Entry"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )


@router.delete(path="/country/{country_id}/city/{city_id}", tags=["city"])
async def delete_entry(request: Request, city_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            country_dal = CityDAL(session)
            try:
                await country_dal.delete_entry(city_id)
                return JSONResponse(
                    status_code=200,
                    content={"message": "Continent Entry Deleted"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )
