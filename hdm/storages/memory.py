from collections import defaultdict
from typing import Iterable, Optional

from hdm.storages import Storage
from hdm.types.mappings import ResultMapping
from hdm.types.entity import Entity


class MemoryStorage(Storage):
    def __init__(self):
        self._tables = defaultdict(dict)
        self._autoincrements = defaultdict(int)
        self._query_count = 0

    def setup(self):
        pass

    def delete(self, entity: Entity) -> Entity:
        pass

    def find_one(self, tablename: str, criteria: dict) -> Optional[ResultMapping]:
        for row in self.find_many(tablename, criteria, limit=1):
            return row

    def find_many(
        self, tablename: str, criteria: dict, *, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Iterable[ResultMapping]:
        limit, offset = max(limit, 0) if limit is not None else None, max(offset or 0, 0)
        current = 0

        for row in self._tables[tablename].values():
            # Stop if limit is reached, implemented here to support limit=0
            if limit is not None and current >= limit:
                break

            # Check if row matches criteria
            for k, v in criteria.items():
                if row.get(k) != v:
                    break

            # Yield row if all criteria are met
            else:
                # ... but not until offset is reached
                if offset > 0:
                    offset -= 1
                    continue

                yield row
                current += 1

    def insert(self, tablename: str, values: dict) -> ResultMapping:
        if "id" not in values:
            self._autoincrements[tablename] += 1
            identity = {"id": str(self._autoincrements[tablename])}
        else:
            identity = {"id": values["id"]}

        self._tables[tablename][identity["id"]] = {**values, **identity}

        return identity

    def update(self, tablename: str, criteria: dict, values: dict) -> None:
        if (row := self.find_one(tablename, criteria)) is not None:
            self._tables[tablename][row["id"]] = {**row, **values}
            return self._tables[tablename][row["id"]]
        raise ValueError("Row not found, cannot update.")
