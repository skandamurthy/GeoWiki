from typing import Any

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base: Any = declarative_base()


async def get_datastore(return_key="session"):
    db_URL = URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password="1234",
        host="localhost",
        port=5432,
        database="postgres",
    )
    engine = create_async_engine(db_URL, future=True, echo=False, pool_pre_ping=True)
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession,
    )
    if return_key == "session":
        return async_session
    elif return_key == "engine":
        return engine
