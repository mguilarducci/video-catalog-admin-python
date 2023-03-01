from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

from __shared.domain.entities import Entity
from __shared.domain.value_objects import UniqueEntityId


GenericEntity = TypeVar('GenericEntity', bound=Entity)
GenericSearchableInput = TypeVar('GenericSearchableInput')
GenericSearchableOutput = TypeVar('GenericSearchableOutput')


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


class SearchableRepositoryInterface(Generic[GenericEntity,
                                            GenericSearchableInput,
                                            GenericSearchableOutput],
                                    RepositoryInterface[GenericEntity], ABC):
    @abstractmethod
    def search(self, params: GenericSearchableInput) -> GenericSearchableOutput:
        raise NotImplementedError()


SearchFilter = TypeVar('SearchFilter', str, Any)


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[SearchFilter]):
    DEFAULT_PAGE = 1
    DEFAULT_ITEMS_PER_PAGE = 10
    DEFAULT_ORDER_BY_FIELD = None
    DEFAULT_ORDER_BY_DIRECTION = None
    DEFAULT_FILTER = None

    page: Optional[int] = field(
        default_factory=lambda: SearchParams.DEFAULT_PAGE)
    items_per_page: Optional[int] = field(
        default_factory=lambda: SearchParams.DEFAULT_ITEMS_PER_PAGE)
    order_by_field: Optional[str] = field(
        default_factory=lambda: SearchParams.DEFAULT_ORDER_BY_FIELD)
    order_by_direction: Optional[str] = field(
        default_factory=lambda: SearchParams.DEFAULT_ORDER_BY_DIRECTION)
    filter: Optional[SearchFilter] = field(
        default_factory=lambda: SearchParams.DEFAULT_FILTER)

    def __post_init__(self):
        self._normalize_page()
        self._normalize_items_per_page()
        self._normalize_order_by_field()
        self._normalize_order_by_direction()
        self._normalize_filter()

    def _normalize_page(self):
        page = SearchParams._convert_to_int(self.page)
        if page <= 0:
            page = SearchParams.DEFAULT_PAGE

        self.page = page

    def _normalize_items_per_page(self):
        items_per_page = SearchParams._convert_to_int(self.items_per_page)
        if items_per_page < 1:
            items_per_page = SearchParams.DEFAULT_ITEMS_PER_PAGE

        self.items_per_page = items_per_page

    def _normalize_order_by_field(self):
        if self.order_by_field is not None:
            self.order_by_field = None if self.order_by_field == '' \
                else str(self.order_by_field)

    def _normalize_order_by_direction(self):
        if not self.order_by_field:
            self.order_by_direction = None
            return

        direction = str(self.order_by_direction).lower()
        if direction not in ['asc', 'desc']:
            self.order_by_direction = 'asc'
            return

        self.order_by_direction = direction

    def _normalize_filter(self):
        if self.filter is not None:
            self.filter = None if self.filter == '' \
                else str(self.filter)

    @staticmethod
    def _convert_to_int(value: Any, default=0) -> int:  # pylint: disable=no-self-use
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
