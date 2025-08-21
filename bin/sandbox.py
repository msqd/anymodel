from argparse import Namespace
from typing import Optional

from anymodel.mapper import Mapper
from anymodel.storages.memory import MemoryStorage

from anymodel import Collection, Entity
from anymodel.types.relations import OneToManyRelation

mappers = Namespace()


class Ability(Entity):
    id: Optional[int] = None
    name: str
    hero_id: Optional[int] = None


class Hero(Entity):
    id: Optional[int] = None
    name: str
    abilities: Collection[Ability]


primary_storage = MemoryStorage()
secondary_storage = MemoryStorage()


mappers.abilities = Mapper(
    Ability,
    fields=("id", "name", "hero_id"),
    storage=primary_storage,
    secondary_storages={"secondary": secondary_storage},
)
mappers.heroes = Mapper(
    Hero,
    fields=("id", "name"),
    relations={
        "abilities": OneToManyRelation(mappers.abilities),
    },
    storage=primary_storage,
)

batman = Hero(name="Batman", abilities=[Ability(name="Rich")])
superman = Hero(name="Superman", abilities=[Ability(name="Flying"), Ability(name="Laser Eyes")])

mappers.heroes.save(batman)
mappers.heroes.save(superman)

print(list(mappers.abilities.find()))

heroes = [
    mappers.heroes.find_one_by_pk(1),
    mappers.heroes.find_one_by_pk(2),
]

for hero in heroes:
    hero.abilities.load()
    print(hero.name, "->", hero)
