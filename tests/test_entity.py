from ._models import Hero


def test_modified_fields():
    hero = Hero(name="Superman")

    assert not hero.is_clean()
    assert hero.model_fields_set == {"name"}

    hero.set_clean()

    assert hero.is_clean()
    assert hero.model_fields_set == set()

    hero.id = 42
    hero.name = "Batman"

    assert not hero.is_clean()
    assert hero.model_fields_set == {"id", "name"}


def test_identity():
    # is identity at the right place ? does not make much sense out of a mapping context
    hero = Hero(name="Superman")
    assert hero.get_identity() is None

    hero.set_identity({"id": 42})
    assert hero.get_identity() == {"id": 42}

    hero.detach()
    assert hero.get_identity() is None
