from typing import MutableMapping, Mapping

from hdm.storages import Storage


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
