from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Generic, List

from __shared.domain.exceptions import NotFoundException
from __shared.domain.repositories import GenericEntity, RepositoryInterface, \
    SearchFilter, SearchParams, SearchResult, SearchableRepositoryInterface
from __shared.domain.value_objects import UniqueEntityId


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[GenericEntity], ABC):
    data: Dict[str, GenericEntity] = field(default_factory=lambda: {})

    def insert(self, entity: GenericEntity) -> None:
        self.data.update({entity.id: entity})

    def find_by_id(self, entity_id: str | UniqueEntityId) -> GenericEntity:
        self._raise_if_not_found(str(entity_id))
        return self.data.get(str(entity_id))

    def find_all(self) -> List[GenericEntity]:
        return list(self.data.values())

    def update(self, entity: GenericEntity) -> None:
        self._raise_if_not_found(entity.id)
        self.data.update({entity.id: entity})

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        self._raise_if_not_found(str(entity_id))
        self.data.pop(str(entity_id))

    def _raise_if_not_found(self, entity_id: str) -> None:
        if entity_id not in self.data:
            raise NotFoundException(
                f'Entity not found. data=[id: `{entity_id}`]')


class InMemorySearchableRepository(Generic[GenericEntity, SearchFilter],
                                   InMemoryRepository[GenericEntity],
                                   SearchableRepositoryInterface[GenericEntity,
                                                                 SearchParams[SearchFilter],
                                                                 SearchResult[GenericEntity]],
                                   ABC):
    def search(self, search_params: SearchParams[SearchFilter]) -> SearchResult[GenericEntity]:
        filtered_data = self._filter(self.data, search_params.filter)
        ordered_data = self._order_by(filtered_data,
                                      search_params.order_by_field,
                                      search_params.order_by_direction)
        paginated_data = self._paginate(ordered_data,
                                        search_params.page,
                                        search_params.items_per_page)

        return SearchResult(count=len(filtered_data),
                            items_per_page=search_params.items_per_page,
                            current_page=search_params.page,
                            data=paginated_data)

    @abstractmethod
    def _filter(self,
                data: List[GenericEntity],
                filter_param: SearchFilter | None) -> List[GenericEntity]:
        raise NotImplementedError()

    def _order_by(self,
                  data: List[GenericEntity],
                  order_by_field: str | None,
                  order_by_direction: str | None) -> List[GenericEntity]:
        if order_by_field not in self.sortable_fields():
            return data

        reverse = order_by_direction == 'desc'
        return sorted(data,
                      key=lambda item: str(
                          getattr(item, order_by_field)).lower(),
                      reverse=reverse)

    def _paginate(self, data: List[GenericEntity], page: int, per_page: int) -> List[GenericEntity]:
        start = (page - 1) * per_page
        end = start + per_page
        return data[slice(start, end)]
