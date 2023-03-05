from typing import List, Optional
from __shared.infra.repositories import InMemorySearchableRepository
from category.domain.entities import Category
from category.domain.repositories import CategoryRepositoryInterface


class CategoryInMemoryRepository(CategoryRepositoryInterface, InMemorySearchableRepository):
    def sortable_fields(self) -> List[str]:
        return ['name', 'created_at']

    def _filter(self, data: List[Category], filter_param: Optional[str]) -> List[Category]:
        return super()._filter(data, filter_param)
