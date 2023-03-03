from dataclasses import dataclass
from typing import List
from unittest import TestCase

from __shared.domain.entities import Entity
from __shared.domain.exceptions import NotFoundException
from __shared.infra.repositories import InMemoryRepository, InMemorySearchableRepository


@dataclass(slots=True, frozen=True, kw_only=True)
class EntityStub(Entity):
    name: str
    age: int


class StubInMemoryRepository(InMemoryRepository[EntityStub]):
    pass


class InMemoryRepositoryUnitTest(TestCase):
    repo: StubInMemoryRepository
    item: EntityStub

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()
        self.item = EntityStub(name='Stub name', age=20)

    def test_should_init_with_empty_data(self):
        self.assertDictEqual({}, self.repo.data)

    def test_insert_should_insert_an_item(self):
        self.repo.insert(self.item)
        self.assertDictEqual({self.item.id: self.item}, self.repo.data)

    def test_insert_should_not_duplicate_an_item(self):
        self.repo.insert(self.item)
        self.repo.insert(self.item)
        self.assertDictEqual({self.item.id: self.item}, self.repo.data)

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

        new_item = EntityStub(name='new', age=30)
        self.repo.insert(new_item)
        items = self.repo.find_all()
        self.assertEqual([self.item, new_item], items)

    def test_update_should_update_an_item(self):
        self.repo.insert(self.item)
        item_updated = EntityStub(
            unique_entity_id=self.item.id, name='new name', age=50)

        self.repo.update(item_updated)
        self.assertEqual(item_updated, self.repo.data.get(self.item.id))

    def test_update_should_raise_an_exception_when_the_item_does_not_exist(self):
        with self.assertRaises(NotFoundException) as error:
            self.repo.update(self.item)

        message_expected = f'Entity not found. data=[id: `{self.item.id}`]'
        self.assertEqual(message_expected, error.exception.args[0])

    def test_delete_should_delete_the_item(self):
        self.repo.insert(self.item)
        self.repo.delete(self.item.id)
        self.assertDictEqual({}, self.repo.data)

    def test_delete_should_raise_an_error_when_the_item_does_not_exist(self):
        with self.assertRaises(NotFoundException) as error:
            self.repo.delete(self.item.id)

        message_expected = f'Entity not found. data=[id: `{self.item.id}`]'
        self.assertEqual(message_expected, error.exception.args[0])


class InMemorySearchableRepositoryStub(InMemorySearchableRepository[EntityStub, str]):
    def _filter(self, data: List[EntityStub], filter_param: str | None) -> List[EntityStub]:
        if not filter_param:
            return data

        filtered = filter(lambda item: filter_param.lower() in item.name.lower()
                          or filter_param == str(item.age), data)

        return list(filtered)


class InMemorySearchableRepositoryUnitTest(TestCase):
    repository: InMemorySearchableRepositoryStub

    def setUp(self) -> None:
        self.repository = InMemorySearchableRepositoryStub()

    def test__filter_behavior(self):
        # pylint: disable=protected-access
        data = [EntityStub(name='name value te', age=20),
                EntityStub(name='Name value', age=30),
                EntityStub(name='test', age=40),]
        result = self.repository._filter(data, None)
        self.assertListEqual(data, result)

        result = self.repository._filter(data, 'name')
        expected = [data[0], data[1]]
        self.assertListEqual(expected, result)

        result = self.repository._filter(data, 'TEST')
        expected = [data[2]]
        self.assertListEqual(expected, result)

        result = self.repository._filter(data, 'TE')
        expected = [data[0], data[2]]
        self.assertListEqual(expected, result)

        result = self.repository._filter(data, '20')
        expected = [data[0]]
        self.assertListEqual(expected, result)
