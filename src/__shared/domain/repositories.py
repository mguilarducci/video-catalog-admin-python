from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import math
from typing import Any, Dict, Generic, List, Optional, TypeVar

from __shared.domain.entities import Entity
from __shared.domain.value_objects import UniqueEntityId


GenericEntity = TypeVar('GenericEntity', bound=Entity)
GenericSearchableInput = TypeVar('GenericSearchableInput')
GenericSearchableOutput = TypeVar('GenericSearchableOutput')
SearchFilter = TypeVar('SearchFilter', str, Any)


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
    def search(self, search_params: GenericSearchableInput) -> GenericSearchableOutput:
        raise NotImplementedError()

    @abstractmethod
    def sortable_fields(self) -> List[str]:
        raise NotImplementedError()


@dataclass(slots=True, kw_only=True, frozen=True)
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

        object.__setattr__(self, 'page', page)

    def _normalize_items_per_page(self):
        items_per_page = SearchParams._convert_to_int(self.items_per_page)
        if items_per_page < 1:
            items_per_page = SearchParams.DEFAULT_ITEMS_PER_PAGE

        object.__setattr__(self, 'items_per_page', items_per_page)

    def _normalize_order_by_field(self):
        if self.order_by_field is not None:
            order_by_field = None if self.order_by_field == '' \
                else str(self.order_by_field)

            object.__setattr__(self, 'order_by_field', order_by_field)

    def _normalize_order_by_direction(self):
        if not self.order_by_field:
            object.__setattr__(self, 'order_by_direction', None)
            return

        direction = str(self.order_by_direction).lower()
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        object.__setattr__(self, 'order_by_direction', direction)

    def _normalize_filter(self):
        if self.filter is not None:
            filter_param = None if self.filter == '' \
                else str(self.filter)

            object.__setattr__(self, 'filter', filter_param)

    @staticmethod
    def _convert_to_int(value: Any, default=0) -> int:  # pylint: disable=no-self-use
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchResult(Generic[GenericEntity]):
    count: int
    items_per_page: int
    current_page: int
    current_page_count: int = field(init=False)
    last_page: int = field(init=False)
    data: List[GenericEntity]

    def __post_init__(self):
        self._normalize_data()
        self._init_current_page_count()
        self._init_last_page()

    def to_dict(self) -> Dict:
        return {'count': self.count,
                'items_per_page': self.items_per_page,
                'current_page': self.current_page,
                'current_page_count': self.current_page_count,
                'last_page': self.last_page,
                'data': self.data}

    def _init_current_page_count(self):
        object.__setattr__(self, 'current_page_count', len(self.data))

    def _init_last_page(self):
        last_page = math.ceil(self.count / self.items_per_page)
        object.__setattr__(self, 'last_page', last_page)

    def _normalize_data(self):
        if self.data is None:
            object.__setattr__(self, 'data', [])
