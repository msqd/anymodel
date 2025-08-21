from typing import Optional

from anymodel import Entity, Field


class Hero(Entity):
    id: Optional[int] = Field(None, primary_key=True)
    name: str


class SuperPower(Entity):
    id: Optional[int] = Field(None, primary_key=True)
    name: str
