from typing import Sequence, Any, Self

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Collection(Sequence):
    def __init__(self, seq_or_loader):
        if callable(seq_or_loader):
            self._loader = seq_or_loader
            self._wrapped = None
        else:
            self._loader = None
            self._wrapped = list(seq_or_loader)

    def load(self):
        if self._loader:
            self._wrapped = list(self._loader())
            self._loader = None

    def __getitem__(self, item):
        self.load()
        return self._wrapped[item]

    def __len__(self):
        self.load()
        return len(self._wrapped)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.list_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.list_schema(),
            ),
        )

    @staticmethod
    def _validate(value) -> "Collection":
        return Collection(value)

    @staticmethod
    def _serialize(value: "Collection") -> Sequence:
        return value._wrapped

    def __repr__(self):
        if self._loader:
            return "..."
        return repr(self._wrapped)


