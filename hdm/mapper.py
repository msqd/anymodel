from typing import Type, TypeVar, Iterable, TYPE_CHECKING, MutableMapping, Optional, Mapping

from pyheck import snake

from hdm.types.collections import Collection
from hdm.types.entity import Entity
from hdm.utilities.identity_map import IdentityMap

if TYPE_CHECKING:
    from hdm.storages import Storage
    from hdm.types.relations import Relation

TConcreteEntity = TypeVar("TConcreteEntity", bound=Entity)

_default = "default"


class Mapper[TMappedEntity]:
    __type__: Type[TMappedEntity] = None
    __tablename__: str = None

    primary_key: Iterable[str] = ("id",)
    fields: Iterable[str] = ()
    relations: Mapping[str, "Relation"] = None

    storages: MutableMapping[str, "Storage"]

    _cache: Optional[IdentityMap] = None

    def __new__(cls, *args, **kwargs):
        new_object = super().__new__(cls)

        try:
            inferred_type = cls.__orig_bases__[0].__args__[0]
        except (AttributeError, IndexError):
            inferred_type = None
        if (
            new_object.__type__ is None
            and inferred_type
            and (inferred_type is not TMappedEntity)
            and issubclass(inferred_type, Entity)
        ):
            new_object.__type__ = inferred_type

        if isinstance(new_object.primary_key, str):
            new_object.primary_key = (new_object.primary_key,)

        return new_object

    def __init__(
        self,
        entity_type: Optional[Type[Entity]] = None,
        *,
        fields: Optional[Iterable[str]] = None,
        relations: Optional[Mapping[str, "Relation"]] = None,
        storage: "Storage",
        secondary_storages: Optional[Mapping[str, "Storage"]] = None,
        cache: Optional[IdentityMap] = None,
    ):
        self.__type__ = self.__type__ or entity_type
        if self.__type__ is None:
            raise ValueError("Entity type not defined at mapper initialization time.")

        if self.__tablename__ is None:
            self.__tablename__ = snake(self.__type__.__name__)

        self.fields = fields or self.fields
        self.relations = relations or self.relations or {}
        self.storages = {_default: storage, **(secondary_storages or {})}

        self._cache = cache

    def add_storage(self, storage: "Storage", *, alias=_default):
        if alias in self.storages:
            raise ValueError(f"Storage '{alias}' already defined for mapper '{self}'.")

        self.storages[alias] = storage

    def save(self, entity: TMappedEntity) -> TMappedEntity:
        """Saves an entity to the database, either inserting (if not mapped yet) or updating it (if a mapping identity
        is present)."""
        print(entity)
        storage = self.storages[_default]
        values = self._get_known_modified_values(entity)
        related_values = self._get_known_modified_related_values(entity)
        print(
            f"{self.__tablename__} {type(self).__name__}::save(values=",
            values,
            ", related_values=",
            related_values,
            ")",
            sep="",
        )

        if (identity := entity.get_identity()) is not None:
            # existing object, update
            storage.update(self.__tablename__, identity, values)
            entity.__pydantic_fields_set__ = entity.__pydantic_fields_set__.difference(values.keys())
        else:
            # new object, insert
            new_identity = storage.insert(self.__tablename__, values)
            entity.set_identity(new_identity)

        for _field, _related_entities in related_values.items():
            relation = self.relations[_field]
            for _related_entity in _related_entities:
                relation.save(self, entity, _related_entity)

        return self._mapped(entity)

    def find_one_by_pk(self, *pk) -> TMappedEntity:
        """Find an entity by its primary key."""

        storage = self.storages[_default]

        if len(pk) != len(self.primary_key):
            raise ValueError(f"Expected {len(self.primary_key)} arguments, got {len(pk)}.")

        # xxx this may be a bit naive, cast all into string will show limits (maybe)
        pk = tuple(map(str, pk))
        if self._cache is not None and (cached := self._cache.get(pk)) is not None:
            return cached
        identity = dict(zip(self.primary_key, pk))

        # find, return None if not found
        if (row := storage.find_one(self.__tablename__, identity)) is None:
            return None

        relations = {k: Collection(relation.get_find_callback_for(self, row)) for k, relation in self.relations.items()}

        entity = self.__type__.model_construct(**row, **relations)
        entity.set_identity(identity)
        entity.set_clean()
        return self._mapped(entity)

    def find(self, **criteria) -> Iterable[TMappedEntity]:
        storage = self.storages[_default]
        for row in storage.find_many(self.__tablename__, criteria):
            entity = self.__type__.model_construct(**row)
            entity.set_identity({k: row[k] for k in self.primary_key})
            entity.set_clean()
            yield self._mapped(entity)

    ### rework needed

    def delete(self, entity: TMappedEntity):
        return self.storages.delete(entity)

    ### (semi) private, don't use out of this class

    def _mapped(self, entity: TMappedEntity) -> TMappedEntity:
        """Make sure an entity is present in the cache."""
        pk = tuple((str(getattr(entity, x)) for x in self.primary_key))
        return self._cache.set(pk, entity) if self._cache is not None else entity

    def _get_known_modified_values(self, entity: TMappedEntity) -> dict:
        """Gets a dict of changed values for the given entity, but limited to the fields we know about."""
        return {k: getattr(entity, k) for k in entity.model_fields_set if k in self.fields}

    def _get_known_modified_related_values(self, entity: TMappedEntity) -> Mapping[str, Entity]:
        """Gets a dict of changed values for the given entity, but limited to the fields we know about."""
        return {k: getattr(entity, k) for k in entity.model_fields_set if k in self.relations}
