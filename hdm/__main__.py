from typing_extensions import Optional

from hdm.types.entity import Entity
from hdm.mapper import Mapper
from hdm.storages.sqlalchemy import SqlAlchemyStorage


class Restaurant(Entity):
    id: Optional[int] = None
    name: str = ""
    address: str = ""
    phone: str = ""


class RestaurantMapper(Mapper[Restaurant]):
    __type__ = Restaurant
    __tablename__ = "restaurants"

    fields = ["name", "address", "phone"]
    primary_key = "id"


def main():
    storage = SqlAlchemyStorage("postgresql://postgres:postgres@localhost:5432")
    mapper = RestaurantMapper(storage)
    storage.setup()
    mapper.save(Restaurant(name="test"))


if __name__ == "__main__":
    main()
