from typing import Union, Any, override, Optional, Iterable

from sqlalchemy import URL, create_engine, MetaData, Column, Integer, String, Table

from hdm.types.entity import Entity
from hdm.storages import Storage, ResultMapping
from hdm.utilities.migrations import automigrate


class SqlAlchemyStorage(Storage):
    def __init__(self, url: Union[str, URL], **kwargs: Any):
        self.engine = create_engine(url, **kwargs)
        self.metadata = MetaData()
        self.tables = {}

    def insert(self, tablename: str, values: dict) -> ResultMapping:
        """Insert a new row into the table, returns the newly generated primary key."""
        table = self.tables[tablename]

        with self.engine.connect() as conn:
            result = conn.execute(table.insert().values(values))
            conn.commit()

        return result.inserted_primary_key._mapping

    def update(self, tablename: str, identity: dict, values: dict) -> None:
        """Updates an existing row in the table."""
        table = self.tables[tablename]
        criteria = _as_criteria(table, identity)

        with self.engine.connect() as conn:
            conn.execute(table.update().where(*criteria).values(values))
            conn.commit()

    @override
    def find_one(self, tablename: str, criteria: dict) -> Optional[ResultMapping]:
        table = self.tables[tablename]
        criteria = _as_criteria(table, criteria)

        query = table.select().where(*criteria)
        with self.engine.connect() as conn:
            result = conn.execute(query)
            row = result.fetchone()
            if row is None:
                return None
            return row._mapping

    @override
    def find_many(self, tablename: str, criteria: dict, *, limit=None, offset=None) -> Iterable[ResultMapping]:
        table = self.tables[tablename]
        criteria = _as_criteria(table, criteria)

        query = table.select().where(*criteria)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        with self.engine.connect() as conn:
            result = conn.execute(query)
            for row in result:
                yield row._mapping

    ### rework (or work) needed

    @override
    def delete(self, entity: Entity) -> Entity:
        ...
        return entity

    @override
    def add_table(self, tablename: str, primary_key: Iterable[str], fields: Iterable[str]):
        if tablename in self.tables:
            raise ValueError(f'Table for "{tablename}" already registered.')

        columns = []

        for field in primary_key:
            columns.append(Column(field, Integer, primary_key=True))

        for field in fields:
            columns.append(Column(field, String))

        self.tables[tablename] = Table(tablename, self.metadata, *columns)

    @override
    def setup(self):
        automigrate(self.engine, self.metadata)


def _as_criteria(table: Table, criteria: dict[str, Any]) -> list:
    return [getattr(table.c, col) == val for col, val in criteria.items()]
