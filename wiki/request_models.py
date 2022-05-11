from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ContinentClass(BaseModel):
    name: str = Field(description="")
    population: int = Field(description="")
    area_in_sq_meters: int = Field(description="")

    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias).get("properties").keys())


class CountryClass(BaseModel):
    name: str = Field(description="")
    population: int = Field(description="")
    area_in_sq_meters: int = Field(description="")
    number_of_roads: Optional[int] = Field(description="")
    number_of_trees: Optional[int] = Field(description="")
    continent_id: int = Field(description="")


class CityClass(BaseModel):
    name: str = Field(description="")
    population: int = Field(description="")
    area_in_sq_meters: int = Field(description="")
    country_id: int = Field(description="")
