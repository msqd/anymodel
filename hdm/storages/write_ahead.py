from typing import Optional, Iterable

from .base import Storage
from ..types.mappings import ResultMapping, ResultMappingView


class WriteAheadStorage(Storage):
    def __init__(self, short_storage: Storage, long_storage: Storage):
        self.short_storage = short_storage
        self.long_storage = long_storage

    def find_one(self, tablename: str, criteria: dict) -> Optional[ResultMapping]:
        if (result := self.short_storage.find_one(tablename, criteria)) is not None:
            return ResultMappingView(result, store="short")

        if (result := self.long_storage.find_one(tablename, criteria)) is not None:
            return ResultMappingView(result, store="long")

    def find_many(self, tablename: str, criteria: dict, *, limit=None, offset=None) -> Iterable[ResultMapping]:
        return self.short_storage.find_many(tablename, criteria, limit=limit, offset=offset)

    def insert(self, tablename: str, values: dict) -> ResultMapping:
        return ResultMappingView(self.short_storage.insert(tablename, values), store="short")

    def update(self, tablename: str, identity: dict, values: dict) -> None:
        return self.short_storage.update(tablename, identity, values)

    def delete(self, tablename, identity: dict):
        # XXX should we delete from both ? how to chose which one to use ?
        return self.short_storage.delete(tablename, identity)

    def archive(self, tablename: str):
        for entity in self.short_storage.find_all():
            self.long_storage.insert(tablename, entity)
            self.short_storage.delete(tablename, {"id": entity["id"]})
