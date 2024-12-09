from abc import abstractmethod, ABC

from hdm.mapper import Mapper


class Relation(ABC):
    @abstractmethod
    def get_find_callback_for(self, mapper, entity):
        raise NotImplementedError

    @abstractmethod
    def save(self, mapper, entity, related_entity):
        raise NotImplementedError


class OneToManyRelation(Relation):
    def __init__(self, mapper: Mapper):
        self.mapper = mapper

    def get_find_callback_for(self, mapper, row):
        def load():
            return self.mapper.find(**{f"{mapper.__tablename__}_id": str(row["id"])})

        return load

    def save(self, mapper, entity, related_entity):
        setattr(related_entity, f"{mapper.__tablename__}_id", entity.id)
        return self.mapper.save(related_entity)
