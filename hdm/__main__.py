from typing_extensions import Optional

from hdm.entity import Entity
from hdm.mapper import Mapper
from hdm.storage import SqlAlchemyStorage


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
    storage.upgrade()
    mapper.save(Restaurant(name="test"))


if __name__ == "__main__":
    main()
