from dataclasses import dataclass
from unittest import TestCase

from __shared.domain.entities import Entity
from __shared.domain.exceptions import NotFoundException
from __shared.infra.repositories import InMemoryRepository


@dataclass(slots=True, frozen=True, kw_only=True)
class StubEntity(Entity):
    name: str
    age: int


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class InMemoryRepositoryUnitTest(TestCase):
    repo: StubInMemoryRepository
    item: StubEntity

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()
        self.item = StubEntity(name='Stub name', age=20)

    def test_should_init_with_empty_data(self):
        self.assertDictEqual({}, self.repo.items)

    def test_insert_should_insert_an_item(self):
        self.repo.insert(self.item)
        self.assertDictEqual({self.item.id: self.item}, self.repo.items)

    def test_insert_should_not_duplicate_an_item(self):
        self.repo.insert(self.item)
        self.repo.insert(self.item)
        self.assertDictEqual({self.item.id: self.item}, self.repo.items)

    def test_find_by_id_should_return_the_item(self):
        self.repo.insert(self.item)
        result = self.repo.find_by_id(self.item.id)
        self.assertEqual(self.item, result)

    def test_find_by_id_should_raise_an_exception_when_the_item_does_not_exist(self):
        with self.assertRaises(NotFoundException) as error:
            self.repo.find_by_id(self.item.id)

        message_expected = f'Entity not found. data=[id: `{self.item.id}`]'
        self.assertEqual(message_expected, error.exception.args[0])

    def test_find_all_should_return_all_items(self):
        items = self.repo.find_all()
        self.assertEqual([], items)

        self.repo.insert(self.item)
        items = self.repo.find_all()
        self.assertEqual([self.item], items)

        new_item = StubEntity(name='new', age=30)
        self.repo.insert(new_item)
        items = self.repo.find_all()
        self.assertEqual([self.item, new_item], items)

    def test_update_should_update_an_item(self):
        self.repo.insert(self.item)
        item_updated = StubEntity(
            unique_entity_id=self.item.id, name='new name', age=50)

        self.repo.update(item_updated)
        self.assertEqual(item_updated, self.repo.items.get(self.item.id))

    def test_update_should_raise_an_exception_when_the_item_does_not_exist(self):
        with self.assertRaises(NotFoundException) as error:
            self.repo.update(self.item)

        message_expected = f'Entity not found. data=[id: `{self.item.id}`]'
        self.assertEqual(message_expected, error.exception.args[0])

    def test_delete_should_delete_the_item(self):
        self.repo.insert(self.item)
        self.repo.delete(self.item.id)
        self.assertDictEqual({}, self.repo.items)

    def test_delete_should_raise_an_error_when_the_item_does_not_exist(self):
        with self.assertRaises(NotFoundException) as error:
            self.repo.delete(self.item.id)

        message_expected = f'Entity not found. data=[id: `{self.item.id}`]'
        self.assertEqual(message_expected, error.exception.args[0])
