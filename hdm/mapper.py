from typing import Type, TypeVar, Iterable, TYPE_CHECKING

from pyheck import snake

from hdm.entity import Entity
from hdm.utilities.identity_map import IdentityMap

if TYPE_CHECKING:
    from hdm.storage import Storage

TConcreteEntity = TypeVar("TConcreteEntity", bound=Entity)


class Mapper[TMappedEntity]:
    __type__: Type[TMappedEntity] = None
    __tablename__: str = None

    primary_key: Iterable[str] = ("id",)
    fields: Iterable[str] = []

    storage: "Storage"

    _cache: IdentityMap

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
        self._cache = IdentityMap()

        self.storage.add_table(self.__tablename__, self.primary_key, self.fields)

    def save(self, entity: TMappedEntity) -> TMappedEntity:
        """Saves an entity to the database, either inserting (if not mapped yet) or updating it (if a mapping identity
        is present)."""
        values = self._get_known_modified_values(entity)

        if (identity := entity.get_identity()) is not None:
            # existing object, update
            self.storage.update(self.__tablename__, identity, values)
            entity.__pydantic_fields_set__ = entity.__pydantic_fields_set__.difference(values.keys())
        else:
            # new object, insert
            new_identity = self.storage.insert(self.__tablename__, values)
            entity.set_identity(new_identity)

        return self._mapped(entity)

    def find_one(self, *pk) -> TMappedEntity:
        """Find an entity by its primary key."""
        if len(pk) != len(self.primary_key):
            raise ValueError(f"Expected {len(self.primary_key)} arguments, got {len(pk)}.")

        # xxx this may be a bit naive, cast all into string will show limits (maybe)
        pk = tuple(map(str, pk))
        if (cached := self._cache.get(pk)) is not None:
            return cached

        identity = dict(zip(self.primary_key, pk))
        row = self.storage.find_one(self.__tablename__, identity)

        if row is None:
            return None

        entity = self.__type__.model_construct(**row)
        entity.set_identity(identity)
        entity.set_clean()
        return self._mapped(entity)

    def find(self, **criteria) -> Iterable[TMappedEntity]:
        for row in self.storage.find_many(self.__tablename__, criteria):
            entity = self.__type__.model_construct(**row)
            entity.set_identity({k: row[k] for k in self.primary_key})
            entity.set_clean()
            yield self._mapped(entity)

    ### rework needed

    def delete(self, entity: TMappedEntity):
        return self.storage.delete(entity)

    ### (semi) private, don't use out of this class

    def _mapped(self, entity: TMappedEntity) -> TMappedEntity:
        """Make sure an entity is present in the cache."""
        pk = tuple((str(getattr(entity, x)) for x in self.primary_key))
        return self._cache.set(pk, entity)

    def _get_known_modified_values(self, entity: TMappedEntity) -> dict:
        """Gets a dict of changed values for the given entity, but limited to the fields we know about."""
        return {k: getattr(entity, k) for k in entity.model_fields_set if k in self.fields}
