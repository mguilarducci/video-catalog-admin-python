from abc import ABC
from dataclasses import asdict, dataclass, field
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

    def _set(self, field_name: str, value: Any):
        object.__setattr__(self, field_name, value)
