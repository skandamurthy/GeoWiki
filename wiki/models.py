from typing import Any

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class Country(Base):
    """
    Country table
    """

    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    area_in_sq_meters = Column(Float, unique=False, nullable=False)
    number_of_hospitals = Column(Integer, unique=False, nullable=True)
    number_of_national_parks = Column(Integer, unique=False, nullable=True)
    created_at = Column(TIMESTAMP, unique=False, nullable=True)
    updated_at = Column(TIMESTAMP, unique=False, nullable=True)
    continent_id = Column(Integer, ForeignKey("continent.id", ondelete="CASCADE"))
    city = relationship("City", backref="country", cascade="all, delete-orphan")


class Continent(Base):
    """
    Continent table
    """

    __tablename__ = "continent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    area_in_sq_meters = Column(Float, unique=False, nullable=False)
    created_at = Column(TIMESTAMP, unique=False, nullable=True)
    updated_at = Column(TIMESTAMP, unique=False, nullable=True)
    country = relationship(Country, backref="continent", cascade="all, delete-orphan")


class City(Base):
    """
    City class table
    """

    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=True)
    area_in_sq_meters = Column(Float, unique=False, nullable=True)
    number_of_roads = Column(Integer, unique=False, nullable=True)
    number_of_trees = Column(Integer, unique=False, nullable=True)
    number_of_hospitals = Column(Integer, unique=False, nullable=True)
    created_at = Column(
        TIMESTAMP,
        unique=False,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(TIMESTAMP, unique=False, nullable=True)
    country_id = Column(Integer, ForeignKey("country.id", ondelete="CASCADE"))
