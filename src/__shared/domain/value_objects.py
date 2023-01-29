from abc import ABC
from dataclasses import dataclass, field, fields
import json
import uuid

from __shared.domain.exceptions import InvalidUniqueEntityIdValueError


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):
    def __str__(self) -> str:
        fields_names = [field.name for field in fields(self)]
        return str(getattr(self, fields_names[0])) \
            if len(fields_names) == 1 \
            else json.dumps({field_name: getattr(self, field_name) for field_name in fields_names})


@dataclass(frozen=True, slots=True)
class UniqueEntityId(ValueObject):
    _id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        id_value = str(self._id) if isinstance(
            self._id, uuid.UUID) else self._id
        object.__setattr__(self, '_id', id_value)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self._id)
        except ValueError as error:
            raise InvalidUniqueEntityIdValueError() from error
