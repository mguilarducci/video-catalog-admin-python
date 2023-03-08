from abc import ABC
from dataclasses import asdict, dataclass, field, _MISSING_TYPE
from typing import Any, Dict

from __shared.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class Entity(ABC):
    # pylint: disable=unnecessary-lambda
    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        return str(self.unique_entity_id)

    def to_dict(self) -> Dict:
        entity_dict = asdict(self)
        entity_dict.pop('unique_entity_id')
        entity_dict['id'] = self.id
        return entity_dict

    @classmethod
    def get_default(cls, field_name: str) -> Any:
        # pylint: disable=no-member
        class_field = cls.__dataclass_fields__.get(field_name)

        if field is None:
            return None

        return None if isinstance(class_field.default, _MISSING_TYPE) else class_field.default

    def _set(self, field_name: str, value: Any) -> None:
        object.__setattr__(self, field_name, value)
