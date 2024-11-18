from typing import Type, TypedDict, Collection, MutableMapping, Mapping

from pyheck.pyheck import snake

from hdm.entity import Entity
from hdm.mapper import IdentityMap
from hdm.storage import Storage
from ._models import Hero


class MemoryTable:
    def __init__(self):
        self._data = {}
        self.__last_id = len(self._data)

    def insert(self, key, values):
        self.__last_id += 1
        self._data[self.__last_id] = {**values, "id": self.__last_id}
        return (self.__last_id,)


class MemoryStorage(Storage):
    _tables = MutableMapping[str, MemoryTable]

    def __init__(self):
        self._tables = {}

    def insert(self, table_name, key: tuple, values: Mapping):
        return self._tables[table_name].insert(key, values)


_Fields = Collection[str]


class _MappedStorage(TypedDict):
    storage: Storage
    key: _Fields
    fields: _Fields


class Mapper:
    __type__: Type[Entity]
    __tablename__: str

    _mappings: list[_MappedStorage]

    def __init__(self, entity_type: Type[Entity], /, *, primary_key: Collection[str] = ("id",)):
        self.__type__ = entity_type
        self.__primary_key__ = primary_key
        self.__fields__ = self.__type__.model_fields
        self.__tablename__ = snake(entity_type.__name__)

        self._mappings = []
        self._cache = IdentityMap()

    def map(self, storage: Storage, fields: Collection[str] | all = all):
        if fields is all:
            fields = list(self.__fields__.keys())

        if len(unknown_fields := (set(fields) - set(self.__fields__.keys()))):
            raise ValueError(
                f"Unknown fields {', '.join(sorted(unknown_fields))} for {self.__type__}, you can only map declared fields."
            )

        self._mappings.append(
            _MappedStorage(
                storage=storage,
                key=self.__primary_key__,
                fields=fields,
            )
        )
        return self

    def store(self, entity: Entity):
        for mapping in self._mappings:
            key = tuple(getattr(entity, k) for k in mapping["key"])
            values = {k: getattr(entity, k) for k in mapping["fields"]}

            new_key = mapping["storage"].insert(self.__tablename__, key, values)

            # set new key values
            for k, v in zip(mapping["key"], new_key):
                setattr(entity, k, v)

            entity.__pydantic_fields_set__ = entity.__pydantic_fields_set__.difference(mapping["key"]).difference(
                mapping["fields"]
            )
        return entity

    def retrieve(self, *key):
        if (cached := self._cache.get(map(str, key))) is not None:
            return cached


def test_basics():
    storage = MemoryStorage()
    mapper = Mapper(Hero).map(storage)
    storage._tables[mapper.__tablename__] = MemoryTable()

    hero = Hero(name="Superman")
    mapper.store(hero)

    assert hero.id == 1
    assert hero.is_clean()

    pass
