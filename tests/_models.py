from typing import Optional

from hdm.types.entity import Entity
from hdm.mapper import Mapper


class Hero(Entity):
    id: Optional[int] = None
    name: str


class HeroMapper(Mapper[Hero]):
    pass
