from dataclasses import dataclass
from typing import List
from unittest import TestCase

from __shared.domain.entities import Entity
from __shared.domain.exceptions import NotFoundException
from __shared.domain.repositories import SearchParams, SearchResult
from __shared.infra.repositories import InMemoryRepository, InMemorySearchableRepository


@dataclass(slots=True, frozen=True, kw_only=True)
class EntityStub(Entity):
    name: str
    age: int
    sortable_int: int


class StubInMemoryRepository(InMemoryRepository[EntityStub]):
    pass


class InMemoryRepositoryUnitTest(TestCase):
    repo: StubInMemoryRepository
    item: EntityStub

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()
        self.item = EntityStub(name='Stub name', age=20, sortable_int=1)

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

        new_item = EntityStub(name='new', age=30, sortable_int=1)
        self.repo.insert(new_item)
        items = self.repo.find_all()
        self.assertEqual([self.item, new_item], items)

    def test_update_should_update_an_item(self):
        self.repo.insert(self.item)
        item_updated = EntityStub(
            unique_entity_id=self.item.id, name='new name', age=50, sortable_int=1)

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
    def sortable_fields(self) -> List[str]:
        return ['name', 'sortable_int']

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
        data = [EntityStub(name='name value te', age=20, sortable_int=1),
                EntityStub(name='Name value', age=30, sortable_int=1),
                EntityStub(name='test', age=40, sortable_int=1),]
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

    def test_get_sortable_fields(self):
        sortable_fields = self.repository.sortable_fields()
        self.assertListEqual(['name', 'sortable_int'], sortable_fields)

    def test__order_by_behavior(self):
        # pylint: disable=protected-access
        data = [EntityStub(name='Test 3', age=3, sortable_int=1), # NOSONAR
                EntityStub(name='TeSt 1', age=1, sortable_int=3), # NOSONAR
                EntityStub(name='test 2', age=2, sortable_int=2)] # NOSONAR

        ordered_name = [data[1], data[2], data[0]]
        ordered_sortable_int = [data[0], data[2], data[1]]

        result = self.repository._order_by(data, None, None)
        self.assertEqual(
            data, result, 'should not sort when field is None')

        result = self.repository._order_by(data, None, 'asc')
        self.assertEqual(
            data, result, 'should not sort when field is None')

        result = self.repository._order_by(data, 'age', None)
        self.assertEqual(
            data, result, 'should not sort when field is not in sortable_fields')

        result = self.repository._order_by(data, 'name', None)
        self.assertEqual(ordered_name, result,
                         'should sort with asc direction when has direction is None')

        result = self.repository._order_by(data, 'name', 'asc')
        self.assertEqual(ordered_name, result,
                         'should sort with asc direction when has direction is `asc`')

        result = self.repository._order_by(data, 'name', 'wtv')
        self.assertEqual(ordered_name, result,
                         'should sort with asc direction when has direction is any other string')

        result = self.repository._order_by(data, 'name', 'desc')
        ordered_name.reverse()
        self.assertEqual(ordered_name, result,
                         'should sort with desc direction when has direction is `desc`')

        result = self.repository._order_by(data, 'sortable_int', None)
        self.assertEqual(ordered_sortable_int, result,
                         'should sort with asc direction when has direction is None')

        result = self.repository._order_by(data, 'sortable_int', 'asc')
        self.assertEqual(ordered_sortable_int, result,
                         'should sort with asc direction when has direction is `asc`')

        result = self.repository._order_by(data, 'sortable_int', 'wtv')
        self.assertEqual(ordered_sortable_int, result,
                         'should sort with asc direction when has direction is any other string')

        result = self.repository._order_by(data, 'sortable_int', 'desc')
        ordered_sortable_int.reverse()
        self.assertEqual(ordered_sortable_int, result,
                         'should sort with desc direction when has direction is `desc`')

    def test__paginate_behavior(self):
        # sourcery skip: extract-duplicate-method
        # pylint: disable=protected-access
        data = [EntityStub(name='A', age=1, sortable_int=1),
                EntityStub(name='B', age=1, sortable_int=1),
                EntityStub(name='C', age=1, sortable_int=1),
                EntityStub(name='D', age=1, sortable_int=1),
                EntityStub(name='E', age=1, sortable_int=1)]

        result = self.repository._paginate(data, 1, 2)
        self.assertEqual(data[:2], result)

        result = self.repository._paginate(data, 2, 2)
        self.assertEqual(data[2:4], result)

        result = self.repository._paginate(data, 3, 2)
        self.assertEqual(data[4:], result)

        result = self.repository._paginate(data, 4, 2)
        self.assertEqual([], result)

        result = self.repository._paginate(data, 1, 3)
        self.assertEqual(data[:3], result)

        result = self.repository._paginate(data, 2, 3)
        self.assertEqual(data[3:], result)

        result = self.repository._paginate(data, 3, 3)
        self.assertEqual([], result)

    def test_search_with_empty_search_params(self):
        self.repository.data = [EntityStub(
            name='a', age=1, sortable_int=1)] * 21

        expected = SearchResult(count=21,
                                items_per_page=10,
                                current_page=1,
                                data=self.repository.data[:10])

        result = self.repository.search(SearchParams())
        self.assertEqual(expected, result)

    def test_search_with_filter_and_order_by(self):
        data = [EntityStub(name='Test 3', age=1, sortable_int=1),
                EntityStub(name='TeSt 1', age=1, sortable_int=1),
                EntityStub(name='C', age=1, sortable_int=1),
                EntityStub(name='test 2', age=1, sortable_int=1),
                EntityStub(name='E', age=1, sortable_int=1)]

        self.repository.data = data

        expected = SearchResult(count=3,
                                items_per_page=10,
                                current_page=1,
                                data=[data[1], data[3], data[0]])

        result = self.repository.search(SearchParams(page=1,
                                                     items_per_page=10,
                                                     filter='test',
                                                     order_by_field='name'))
        self.assertEqual(expected, result)

    def test_search_with_filter_and_paginate(self):
        data = [EntityStub(name='Test 3', age=1, sortable_int=1),
                EntityStub(name='TeSt 1', age=1, sortable_int=1),
                EntityStub(name='C', age=1, sortable_int=1),
                EntityStub(name='test 2', age=1, sortable_int=1),
                EntityStub(name='E', age=1, sortable_int=1)]

        self.repository.data = data

        expected = SearchResult(count=3,
                                items_per_page=2,
                                current_page=1,
                                data=data[:2])

        result = self.repository.search(SearchParams(page=1,
                                                     items_per_page=2,
                                                     filter='test'))
        self.assertEqual(expected, result)

    def test_search_with_order_by_and_paginate(self):
        # sourcery skip: class-extract-method
        data = [EntityStub(name='Test 3', age=1, sortable_int=1),
                EntityStub(name='TeSt 1', age=1, sortable_int=1),
                EntityStub(name='C', age=1, sortable_int=1),
                EntityStub(name='test 2', age=1, sortable_int=1),
                EntityStub(name='E', age=1, sortable_int=1)]

        self.repository.data = data

        expected = SearchResult(count=5,
                                items_per_page=2,
                                current_page=1,
                                data=[data[2], data[4]])

        result = self.repository.search(SearchParams(page=1,
                                                     items_per_page=2,
                                                     order_by_field='name'))

        self.assertEqual(expected, result)

    def test_search_with_filter_and_order_by_and_paginate(self):
        data = [EntityStub(name='Test 3', age=1, sortable_int=1),
                EntityStub(name='TeSt 1', age=1, sortable_int=1),
                EntityStub(name='C', age=1, sortable_int=1),
                EntityStub(name='test 2', age=1, sortable_int=1),
                EntityStub(name='E', age=1, sortable_int=1)]

        self.repository.data = data

        expected = SearchResult(count=3,
                                items_per_page=2,
                                current_page=1,
                                data=[data[1], data[3]])

        result = self.repository.search(SearchParams(page=1,
                                                     items_per_page=2,
                                                     filter='test',
                                                     order_by_field='name'))

        self.assertEqual(expected, result)
