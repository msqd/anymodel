from typing import Type, TypeVar, Iterable, TYPE_CHECKING, MutableMapping
from weakref import WeakValueDictionary

from hdm.entity import Entity

if TYPE_CHECKING:
    from hdm.storage import Storage

TConcreteEntity = TypeVar("TConcreteEntity", bound=Entity)


class Mapper[TMappedEntity]:
    type: Type[TMappedEntity] = None
    name: str = None

    primary_key: Iterable[str] = ("id",)
    fields: Iterable[str] = []

    storage: "Storage"

    # identity map of primary keys to known entities
    _map: MutableMapping[tuple, TMappedEntity]

    def __new__(cls, *args, **kwargs):
        if cls.type is None:
            raise NotImplementedError("Mapper must have a type, the base class cannot be instanciated.")
        if cls.name is None:
            raise NotImplementedError("Mapper must have a name, the base class cannot be instanciated.")

        instance = super().__new__(cls)

        if isinstance(instance.primary_key, str):
            instance.primary_key = (instance.primary_key,)
        return instance

    def __init__(self, storage):
        self.storage = storage
        self.storage.register(self)

        self._map = WeakValueDictionary()

    def save(self, entity: TMappedEntity) -> TMappedEntity:
        entity = self.storage.save(entity)
        return self._store(entity)

    def delete(self, entity: TMappedEntity):
        return self.storage.delete(entity)

    def find(self, *args) -> TMappedEntity:
        """Find an entity by its primary key."""
        if len(args) != len(self.primary_key):
            raise ValueError(f"Expected {len(self.primary_key)} arguments, got {len(args)}.")

        # do we have a cached version?
        if args in self._map:
            return self._map[args]

        # delegate to storage
        return self._store(self.storage.find(self, *args))

    def find_all(self) -> Iterable[TMappedEntity]:
        for entity in self.storage.find_all(self):
            yield self._store(entity)

    def _store(self, entity: TMappedEntity | None):
        if entity is None:
            return None
        identity = entity.get_identity()
        self._map[tuple((identity.get(x) for x in self.primary_key))] = entity
        return entity

    def find_by(self, **kwargs) -> TMappedEntity:
        pass
