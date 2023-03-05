from typing import List
from __shared.infra.repositories import InMemorySearchableRepository
from category.domain.entities import Category
from category.domain.repositories import CategoryRepositoryInterface


class CategoryInMemoryRepository(CategoryRepositoryInterface, InMemorySearchableRepository):
    def sortable_fields(self) -> List[str]:
        return ['name', 'created_at']

    def _filter(self, data: List[Category], filter_param: str | None) -> List[Category]:
        return super()._filter(data, filter_param)
