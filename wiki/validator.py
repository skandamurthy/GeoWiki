from sqlalchemy.future import select
from sqlalchemy.sql import func

from wiki.models import City
from wiki.models import Continent
from wiki.models import Country


async def city_validator(
    data_session,
    country_id: int,
    validator_type: str,
    new_population=None,
    city_id=None,
):
    """
    City Validator Function
    :param data_session:
    :param country_id:
    :param validator_type:
    :param new_population:
    :param city_id:
    :return: Bool
    """
    country_population = (
        await data_session.execute(
            select(Country.population).filter(Country.id == country_id),
        )
    ).one()[0]
    total_city_population = None
    if validator_type == "update":
        total_city_population = (
            await data_session.execute(
                select(func.Sum(City.population)).filter(City.id != city_id),
            )
        ).one()[0]
    if total_city_population:
        total_city_population += new_population
    else:
        total_city_population = new_population
    return total_city_population < country_population


async def country_validator(
    data_session,
    continent_id: int,
    validator_type: str,
    new_population=None,
    country_id=None,
):
    """
    Country Validator Function
    :param data_session:
    :param continent_id:
    :param validator_type:
    :param new_population:
    :param country_id:
    :return: Bool
    """
    continent_population = (
        await data_session.execute(
            select(Continent.population).filter(Continent.id == continent_id),
        )
    ).one()[0]
    total_country_population = None
    if validator_type == "update":
        total_country_population = (
            await data_session.execute(
                select(func.Sum(Country.population)).filter(Country.id != country_id),
            )
        ).one()[0]
    if total_country_population:
        total_country_population += new_population
    else:
        total_country_population = new_population
    return total_country_population < continent_population
