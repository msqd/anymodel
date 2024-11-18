from typing import Union, Any, Optional, Iterable, override

from sqlalchemy import create_engine, MetaData, URL, Table, Column, Integer, String

from hdm.entity import Entity
from hdm.mapper import Mapper
from hdm.utilities.migrations import automigrate


class Storage:
    def register(self, mapper: Mapper): ...
    def upgrade(self): ...
    def save(self, entity: Entity) -> Entity: ...
    def delete(self, entity: Entity) -> Entity: ...
    def find(self, mapper: Mapper, *args) -> Optional[Entity]: ...
    def find_all(self, mapper: Mapper) -> Iterable[Entity]: ...


class SqlAlchemyStorage(Storage):
    def __init__(self, url: Union[str, URL], **kwargs: Any):
        self.engine = create_engine(url, **kwargs)
        self.metadata = MetaData()
        self.tables = {}
        self.mappers = {}

    def get_table_for(self, entity_or_type):
        if isinstance(entity_or_type, Entity):
            entity_or_type = type(entity_or_type)
        return self.tables[entity_or_type]

    def get_mapper_for(self, entity_or_type):
        if isinstance(entity_or_type, Entity):
            entity_or_type = type(entity_or_type)
        return self.mappers[entity_or_type]

    @override
    def register(self, mapper: Mapper):
        if mapper.__type__ in self.mappers:
            raise ValueError(f"Mapper for {mapper.__type__} already registered.")
        self.mappers[mapper.__type__] = mapper

        if mapper.__type__ in self.tables:
            raise ValueError(f"Table for {mapper.__type__} already registered.")

        columns = []

        for field in mapper.primary_key if not isinstance(mapper.primary_key, str) else (mapper.primary_key,):
            columns.append(Column(field, Integer, primary_key=True))

        for field in mapper.fields:
            columns.append(Column(field, String))

        self.tables[mapper.__type__] = Table(mapper.__tablename__, self.metadata, *columns)

    @override
    def upgrade(self):
        automigrate(self.engine, self.metadata)

    @override
    def save(self, entity: Entity) -> Entity:
        mapper, table = self.get_mapper_for(entity), self.get_table_for(entity)
        data = {_name: getattr(entity, _name) for _name in mapper.fields if _name in entity.model_fields_set}

        if identity := entity.get_identity():
            # we know you, let's update
            with self.engine.connect() as conn:
                conn.execute(table.update().where(table.c.id == identity["id"]).values(data))
                conn.commit()
        else:
            # we have a newcomer, let's insert
            with self.engine.connect() as conn:
                result = conn.execute(table.insert().values(data))
                conn.commit()
            entity.set_identity(result.inserted_primary_key._mapping)

        entity.set_clean()
        return entity

    @override
    def delete(self, entity: Entity) -> Entity:
        ...
        return entity

    @override
    def find(self, mapper: Mapper, *args) -> Optional[Entity]:
        table = self.get_table_for(mapper.__type__)
        criteria = _build_where_clause_arguments(table, dict(zip(mapper.primary_key, args)))
        with self.engine.connect() as conn:
            result = conn.execute(table.select().where(*criteria))
            row = result.fetchone()
            if row is None:
                return None
            entity = mapper.__type__.model_construct(**row._mapping)
            entity.set_identity({k: getattr(entity, k) for k in mapper.primary_key})
            entity.set_clean()
            return entity

    @override
    def find_all(self, mapper: Mapper) -> Iterable[Entity]:
        with self.engine.connect() as conn:
            result = conn.execute(self.get_table_for(mapper.__type__).select())
            for row in result:
                entity = mapper.__type__.model_construct(**row._mapping)
                entity.set_identity({k: getattr(entity, k) for k in mapper.primary_key})
                entity.set_clean()
                yield entity


def _build_where_clause_arguments(table: Table, criteria: dict[str, Any]) -> list:
    return [getattr(table.c, col) == val for col, val in criteria.items()]
