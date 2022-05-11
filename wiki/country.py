from typing import List

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from wiki.models import Country
from wiki.request_models import CountryClass
from wiki.validator import country_validator


class CountryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_entry(self, data: CountryClass, continent_id):
        valid_flag = await country_validator(
            self.db_session,
            validator_type="update",
            new_population=data.population,
            continent_id=continent_id,
        )
        if valid_flag:
            new_entry_obj = Country(**data.dict())
            new_entry_obj.continent_id = continent_id
            self.db_session.add(new_entry_obj)
            await self.db_session.commit()
            return new_entry_obj.id
        else:
            return False

    async def get_all_entries(self, continent_id: int) -> List[Country]:
        res = await self.db_session.execute(
            select(Country)
            .filter(Country.continent_id == continent_id)
            .order_by(Country.id),
        )
        return res.scalars().all()

    async def get_entry(self, country_id):
        res = await self.db_session.execute(
            select(Country).filter(Country.id == country_id),
        )
        return res.scalar()

    async def update_entry(
        self,
        data: CountryClass,
        continent_id: int,
        country_id=None,
    ):
        res = update(Country).where(Country.id == country_id)
        valid_flag = await country_validator(
            self.db_session,
            continent_id=continent_id,
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
            await self.db_session.commit()
            return True
        else:
            return False

    async def delete_entry(self, country_id: int):
        # TODO: Find a proper way to delete asynchronously - Currently not available
        res = await self.db_session.execute(
            select(Country).filter(Country.id == country_id),
        )
        res = res.scalar()
        await self.db_session.delete(res)
        await self.db_session.commit()
