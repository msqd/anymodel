from os import PathLike
from typing import Optional, Iterable

from hdm.storages import Storage, ResultMapping
from pathlib import Path



def _get_relative_path_from_criteria(criteria: dict) -> Path:
    if len(criteria) != 1 or "id" not in criteria:
        raise ValueError(f"Only 'id' criteria is supported for this storage type, got {criteria}.")

    if not criteria["id"]:
        raise ValueError(f"Empty 'id' criteria is not supported for this storage type, got {criteria}.")

    pk = str(criteria["id"])


    if len(pk) <= 4:
        return Path('__') / pk
    if len(pk) <= 6:
        return Path(pk[:2]) / '__'/ pk[2:]
    return Path(pk[:2]) / pk[2:4] / pk[4:]


class FileSystemStorage(Storage):
    def __init__(self, path: str | PathLike):
        self.path = Path(path)

    def find_one(self, tablename: str, criteria: dict) -> Optional[ResultMapping]:
        filename = self.path / _get_relative_path_from_criteria(criteria)
        print(filename)
        if not filename.exists():
            return None

        ...
        raise NotImplementedError("XXXXXX")

    def find_many(
            self,
            tablename: str,
            criteria: dict,
            *,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> Iterable[ResultMapping]:
        pass

    def insert(self, tablename: str, values: dict) -> ResultMapping:
        filename = self.path / _get_relative_path_from_criteria({'id': values['id']})
        print(filename)

    def update(self, tablename: str, criteria: dict, values: dict) -> None:
        pass
