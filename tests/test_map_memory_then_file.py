from hdm.mapper import Mapper
from ._models import Hero

class HeroMapper(Mapper[Hero]):
    pass

def test_multimap():
    heroes = HeroMapper()
    heroes.set_storage()

