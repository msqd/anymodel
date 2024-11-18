from sqlite3 import OperationalError
from typing import Optional

from hdm.entity import Entity
from hdm.mapper import Mapper
from hdm.storage import SqlAlchemyStorage
import pytest


class Hero(Entity):
    id: Optional[int] = None
    name: str


class HeroMapper(Mapper[Hero]):
    pass


def test_basics():
    storage = SqlAlchemyStorage("sqlite:///:memory:")
    mapper = HeroMapper(storage)

    hero = Hero(name="Superman")

    with pytest.raises(OperationalError):
        mapper.save(hero)

    storage.upgrade()

    hero = Hero(id=1, name="Superman")
    hero = storage.save(hero)
