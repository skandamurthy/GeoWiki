from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from wiki.continent import ContinentDAL
from wiki.request_models import ContinentClass

router = APIRouter(prefix="/v1/wiki")


@router.post(path="/continent", tags=["continent"])
async def create_entry(request: Request, data: ContinentClass):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            continent_dal = ContinentDAL(session)
            try:
                id_ = await continent_dal.create_entry(data)
                return JSONResponse(
                    status_code=200,
                    content={"id": id_, "message": "Added Continent Entry"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )


@router.get(path="/continent", tags=["continent"])
async def get_all_entries(request: Request):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            continent_dal = ContinentDAL(session)
            try:
                ans = await continent_dal.get_all_entries()
                return ans
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )


@router.patch(path="/continent/{continent_id}", tags=["continent"])
async def update_entry(request: Request, data: ContinentClass, continent_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            continent_dal = ContinentDAL(session)
            try:
                await continent_dal.update_entry(data, continent_id)
                return JSONResponse(
                    status_code=200,
                    content={"message": "Updated Continent Entry"},
                )
            except Exception:
                return JSONResponse(
                    status_code=422,
                    content={"message": "Function Failed"},
                )


@router.delete(path="/books/{continent_id}", tags=["continent"])
async def delete_entry(request: Request, continent_id: int):
    async_session = await request.app.datastore.get_datastore()
    async with async_session() as session:
        async with session.begin():
            continent_dal = ContinentDAL(session)
        try:
            await continent_dal.delete_entry(continent_id)
            return JSONResponse(
                status_code=200,
                content={"message": "Continent Entry Deleted"},
            )
        except Exception:
            return JSONResponse(status_code=422, content={"message": "Function Failed"})
