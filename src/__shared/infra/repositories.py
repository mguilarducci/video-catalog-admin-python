from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List

from __shared.domain.exceptions import NotFoundException
from __shared.domain.repositories import GenericEntity, RepositoryInterface
from __shared.domain.value_objects import UniqueEntityId


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[GenericEntity], ABC):
    items: Dict[str, GenericEntity] = field(default_factory=lambda: {})

    def insert(self, entity: GenericEntity) -> None:
        self.items.update({entity.id: entity})

    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        self._raise_if_not_found(str(entity_id))
        return self.items.get(str(entity_id))

    def find_all(self) -> List[GenericEntity]:
        return list(self.items.values())

    def update(self, entity: GenericEntity) -> None:
        self._raise_if_not_found(entity.id)
        self.items.update({entity.id: entity})

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        self._raise_if_not_found(str(entity_id))
        self.items.pop(str(entity_id))

    def _raise_if_not_found(self, entity_id: str) -> None:
        if entity_id not in self.items:
            raise NotFoundException(f'Entity not found. data=[id: `{entity_id}`]')
