from pydantic import BaseModel

_IDENTITY_ATTRIBUTE = "__identity__"

class Entity(BaseModel):
    def set_clean(self):
        self.__pydantic_fields_set__ = set()

    def get_identity(self) -> dict | None:
        return getattr(self,_IDENTITY_ATTRIBUTE, None)

    def set_identity(self, identity: dict):
        setattr(self, _IDENTITY_ATTRIBUTE, identity)
        self.__dict__.update(identity)

    def detach(self):
        delattr(self, _IDENTITY_ATTRIBUTE)

    def __repr__(self):
        return f"<{type(self).__name__} {super().__str__()}>"
