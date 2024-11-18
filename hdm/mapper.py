from typing import Type, TypeVar, Iterable, TYPE_CHECKING, MutableMapping, Any
from weakref import WeakValueDictionary

from pyheck import snake

from hdm.entity import Entity

if TYPE_CHECKING:
    from hdm.storage import Storage

TConcreteEntity = TypeVar("TConcreteEntity", bound=Entity)


class IdentityMap:
    _map: MutableMapping[tuple, Any]

    def __init__(self):
        self._map = WeakValueDictionary()

    def set(self, key: tuple[str], entity: Entity | None):
        if entity is None:
            return None
        self._map[key] = entity
        return entity

    def get(self, key: Iterable[str]) -> Entity | None:
        return self._map.get(tuple(key))


class Mapper[TMappedEntity]:
    __type__: Type[TMappedEntity] = None
    __tablename__: str = None

    primary_key: Iterable[str] = ("id",)
    fields: Iterable[str] = []

    storage: "Storage"

    map: IdentityMap

    def __new__(cls, *args, **kwargs):
        new_object = super().__new__(cls)

        if new_object.__type__ is None:
            new_object.__type__ = cls.__orig_bases__[0].__args__[0]

        if new_object.__tablename__ is None:
            new_object.__tablename__ = snake(new_object.__type__.__name__)

        if isinstance(new_object.primary_key, str):
            new_object.primary_key = (new_object.primary_key,)

        return new_object

    def __init__(self, storage):
        self.storage = storage

        # xxx circular dependency, let's fix that ?
        self.storage.register(self)
        self.map = IdentityMap()

    def get_identity_tuple(self, obj: TMappedEntity) -> tuple:
        """Returns the ordered primary key values for the given entity."""
        identity = obj.get_identity()
        return tuple((identity.get(x) for x in self.primary_key))

    def save(self, entity: TMappedEntity) -> TMappedEntity:
        entity = self.storage.save(entity)
        return self.map.set(self.get_identity_tuple(entity), entity)

    def delete(self, entity: TMappedEntity):
        return self.storage.delete(entity)

    def find(self, *args: tuple[str]) -> TMappedEntity:
        """Find an entity by its primary key."""
        if len(args) != len(self.primary_key):
            raise ValueError(f"Expected {len(self.primary_key)} arguments, got {len(args)}.")

        if (cached := self.map.get(args)) is not None:
            return cached

        obj = self.storage.find(self, *args)

        return self.map.set()

    def find_all(self) -> Iterable[TMappedEntity]:
        for entity in self.storage.find_all(self):
            yield self._store(entity)

    def find_by(self, **kwargs) -> TMappedEntity:
        pass
