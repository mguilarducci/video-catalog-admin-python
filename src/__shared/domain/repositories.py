from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from __shared.domain.entities import Entity
from __shared.domain.value_objects import UniqueEntityId


GenericEntity = TypeVar('GenericEntity', bound=Entity)


class RepositoryInterface(Generic[GenericEntity], ABC):
    @abstractmethod
    def insert(self, entity: GenericEntity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[GenericEntity]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: GenericEntity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()
