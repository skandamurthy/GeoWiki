from typing import List

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from wiki.models import City
from wiki.request_models import CityClass
from wiki.validator import city_validator


class CityDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_entry(self, data: CityClass, country_id: int):

        valid_flag = await city_validator(
            self.db_session,
            validator_type="update",
            new_population=data.population,
            country_id=country_id,
        )
        if valid_flag:
            new_entry_obj = City(**data.dict())
            self.db_session.add(new_entry_obj)
            await self.db_session.commit()
            return new_entry_obj.id
        else:
            return False

    async def get_all_entries(self, country_id: int) -> List[City]:
        res = await self.db_session.execute(
            select(City).filter(City.country_id == country_id).order_by(City.id),
        )
        return res.all()

    async def get_entry(self, country_id):
        res = await self.db_session.execute(select(City).filter(City.id == country_id))
        return res.scalar()

    async def update_entry(self, data: CityClass, country_id: int, city_id: int):
        res = update(City).where(City.id == country_id)
        valid_flag = await city_validator(
            self.db_session,
            city_id=city_id,
            country_id=country_id,
            validator_type="update",
            new_population=data.population,
        )
        if valid_flag:
            # Only Allowed parameters are allowed to
            if data.name:
                res = res.values(name=data.name)
            if data.population:
                res = res.values(population=data.population)
            if data.area_in_sq_meters:
                res = res.values(area_in_sq_meters=data.area_in_sq_meters)
        res.values(updated_at=current_timestamp)
        res.execution_options(synchronize_session="fetch")
        await self.db_session.execute(res)

    async def delete_entry(self, city_id: int):
        # TODO: Find a proper way to delete asynchronously - Currently not available
        res = await self.db_session.execute(select(City).filter(City.id == city_id))
        res = res.scalar()
        await self.db_session.delete(res)
        await self.db_session.commit()
        return True
