from unittest import TestCase
from __shared.infra.repositories import InMemorySearchableRepository
from category.domain.repositories import CategoryRepositoryInterface

from category.infra.repositories import CategoryInMemoryRepository


class CategoryInMemoryRepositoryUnitTest(TestCase):
    repository: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.repository = CategoryInMemoryRepository()

    def test_should_implements_base_classes(self):
        self.assertTrue(issubclass(CategoryInMemoryRepository,
                        CategoryRepositoryInterface))
        self.assertTrue(issubclass(CategoryInMemoryRepository,
                        InMemorySearchableRepository))

    def test_sortable_fields(self):
        expected = ['name', 'created_at']
        result = self.repository.sortable_fields()

        self.assertListEqual(expected, result)
