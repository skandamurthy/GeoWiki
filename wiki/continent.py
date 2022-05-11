from typing import List

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from wiki.models import Continent
from wiki.request_models import ContinentClass


class ContinentDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_entry(self, data: ContinentClass):
        new_entry_obj = Continent(**data.dict())
        self.db_session.add(new_entry_obj)
        await self.db_session.commit()
        return new_entry_obj.id

    async def get_all_entries(self) -> List[Continent]:
        res = await self.db_session.execute(select(Continent).order_by(Continent.id))
        return res.scalars().all()

    async def get_entry(self, continent_id):
        res = await self.db_session.execute(
            select(Continent).filter(Continent.id == continent_id),
        )
        return res.scalar()

    async def update_entry(self, data: ContinentClass, continent_id: int):
        res = update(Continent).where(Continent.id == continent_id)
        for _, value in data.dict().items():
            res = res.values(_=value)
        # Updated timestamp
        res.values(updated_at=current_timestamp)
        res.execution_options(synchronize_session="fetch")
        await self.db_session.execute(res)
        return True

    async def delete_entry(self, continent_id: int):
        # TODO: Find a proper way to delete asynchronously - Currently not available
        res = await self.db_session.execute(
            select(Continent).filter(Continent.id == continent_id),
        )
        res = res.scalar()
        await self.db_session.delete(res)
        await self.db_session.commit()
        return True
