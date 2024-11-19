from typing import MutableMapping, Any
from weakref import WeakValueDictionary

from hdm.entity import Entity

Identity = tuple[str, ...]


class IdentityMap:
    _map: MutableMapping[Identity, Any]

    def __init__(self):
        self._map = WeakValueDictionary()

    def set(self, key: Identity, entity: Entity | None):
        if entity is None:
            return None
        self._map[key] = entity
        return entity

    def get(self, key: Identity) -> Entity | None:
        return self._map.get(tuple(key))
