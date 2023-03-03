from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase
from __shared.domain.entities import Entity
from __shared.domain.repositories import GenericEntity, RepositoryInterface, \
    SearchFilter, SearchParams, SearchResult, SearchableRepositoryInterface


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityStub(Entity):
    name: str
    age: int


class RepositoryInterfaceUnitTest(TestCase):
    def test_should_implement_methods(self):
        with self.assertRaises(TypeError) as error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()

        expected_message = "Can't instantiate abstract class RepositoryInterface " + \
            "with abstract methods delete, find_all, find_by_id, insert, update"
        self.assertEqual(expected_message, error.exception.args[0])


class SearchableRepositoryInterfaceUnitTest(TestCase):
    def test_should_implement_methods(self):
        with self.assertRaises(TypeError) as error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()

        expected_message = "Can't instantiate abstract class SearchableRepositoryInterface " + \
            "with abstract methods delete, find_all, find_by_id, insert, search, update"
        self.assertEqual(expected_message, error.exception.args[0])


class SearchParamsUnitTest(TestCase):
    def test_should_have_correct_props(self):
        expected = {
            'page': Optional[int],
            'items_per_page': Optional[int],
            'order_by_field': Optional[str],
            'order_by_direction': Optional[str],
            'filter': Optional[SearchFilter]
        }

        result = SearchParams.__annotations__

        self.assertDictEqual(expected, result)

    def test_should_have_correct_default_values(self):
        search_params = SearchParams()

        self.assertEqual(1, search_params.page,
                         'SearchParams.page default value should be `1`')
        self.assertEqual(10, search_params.items_per_page,
                         'SearchParams.items_per_page default value should be `10`')
        self.assertIsNone(search_params.order_by_field,
                          'SearchParams.order_by_field default value should be `None`')
        self.assertIsNone(search_params.order_by_direction,
                          'SearchParams.order_by_direction default value should be `None`')
        self.assertIsNone(search_params.filter,
                          'SearchParams.filter default value should be `None`')

    def test_page_prop_behavior(self):
        cases = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "fake", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': "0", 'expected': 1},
            {'page': "-1", 'expected': 1},
            {'page': 5.5, 'expected': 5},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
        ]

        for case in cases:
            page = case.get('page')
            expected = case.get('expected')
            expected_message = f'`SearchParams(page={page})` should set the ' + \
                f'`SearchParams.page` value to `{expected}`.'

            search_params = SearchParams(page=page)

            self.assertEqual(expected, search_params.page, expected_message)

    def test_items_per_page_behavior(self):
        cases = [
            {'items_per_page': None, 'expected': 10},
            {'items_per_page': "", 'expected': 10},
            {'items_per_page': "fake", 'expected': 10},
            {'items_per_page': 0, 'expected': 10},
            {'items_per_page': -1, 'expected': 10},
            {'items_per_page': "0", 'expected': 10},
            {'items_per_page': "-1", 'expected': 10},
            {'items_per_page': 5.5, 'expected': 5},
            {'items_per_page': True, 'expected': 1},
            {'items_per_page': False, 'expected': 10},
            {'items_per_page': {}, 'expected': 10},
            {'items_per_page': 1, 'expected': 1},
            {'items_per_page': 2, 'expected': 2},
        ]

        for case in cases:
            items_per_page = case.get('items_per_page')
            expected = case.get('expected')
            expected_message = f'`SearchParams(items_per_page={items_per_page})` ' + \
                f'should set the `SearchParams.items_per_page` value to `{expected}`.'

            search_params = SearchParams(items_per_page=items_per_page)

            self.assertEqual(
                expected, search_params.items_per_page, expected_message)

    def test_order_by_field_behavior(self):
        cases = [
            {'order_by_field': None, 'expected': None},
            {'order_by_field': "", 'expected': None},
            {'order_by_field': "fake", 'expected': 'fake'},
            {'order_by_field': 0, 'expected': '0'},
            {'order_by_field': -1, 'expected': '-1'},
            {'order_by_field': "0", 'expected': '0'},
            {'order_by_field': "-1", 'expected': '-1'},
            {'order_by_field': 5.5, 'expected': '5.5'},
            {'order_by_field': True, 'expected': 'True'},
            {'order_by_field': False, 'expected': 'False'},
            {'order_by_field': {}, 'expected': '{}'},
        ]

        for case in cases:
            order_by_field = case.get('order_by_field')
            expected = case.get('expected')
            expected_message = f'`SearchParams(order_by_field={order_by_field})` ' + \
                f'should set the `SearchParams.order_by_field` value to `{expected}`.'

            search_params = SearchParams(order_by_field=order_by_field)

            self.assertEqual(
                expected, search_params.order_by_field, expected_message)

    def test_order_by_direction_behavior(self):
        search_params = SearchParams(order_by_field=None)
        expected_message = '`SearchParams(order_by_field=None)` ' + \
            'should set the `SearchParams.order_by_direction` value to `None`.'  # NOSONAR
        self.assertIsNone(
            search_params.order_by_direction, expected_message)

        search_params = SearchParams(
            order_by_field=None, order_by_direction='asc')
        expected_message = '`SearchParams(order_by_field=None, order_by_direction="asc")` ' + \
            'should set the `SearchParams.order_by_direction` value to `None`.'
        self.assertIsNone(
            search_params.order_by_direction, expected_message)

        search_params = SearchParams(order_by_field='')
        expected_message = '`SearchParams(order_by_field="")` ' + \
            'should set the `SearchParams.order_by_direction` value to `None`.'
        self.assertIsNone(
            search_params.order_by_direction, expected_message)

        search_params = SearchParams(
            order_by_field='', order_by_direction='asc')
        expected_message = '`SearchParams(order_by_field="", order_by_direction="asc")` ' + \
            'should set the `SearchParams.order_by_direction` value to `None`.'
        self.assertIsNone(
            search_params.order_by_direction, expected_message)

        cases = [
            {'order_by_direction': None, 'expected': 'asc'},
            {'order_by_direction': "", 'expected': 'asc'},
            {'order_by_direction': "fake", 'expected': 'asc'},
            {'order_by_direction': 0, 'expected': 'asc'},
            {'order_by_direction': {}, 'expected': 'asc'},
            {'order_by_direction': 'asc', 'expected': 'asc'},
            {'order_by_direction': 'ASC', 'expected': 'asc'},
            {'order_by_direction': 'desc', 'expected': 'desc'},
            {'order_by_direction': 'DESC', 'expected': 'desc'},
        ]

        for case in cases:
            order_by_direction = case.get('order_by_direction')
            expected = case.get('expected')
            expected_message = f'`SearchParams(order_by_direction={order_by_direction})` ' + \
                f'should set the `SearchParams.order_by_direction` value to `{expected}`.'

            search_params = SearchParams(
                order_by_field='field', order_by_direction=order_by_direction)

            self.assertEqual(
                expected, search_params.order_by_direction, expected_message)

    def test_filter_behavior(self):
        cases = [
            {'filter': None, 'expected': None},
            {'filter': "", 'expected': None},
            {'filter': "fake", 'expected': 'fake'},
            {'filter': 0, 'expected': '0'},
            {'filter': -1, 'expected': '-1'},
            {'filter': "0", 'expected': '0'},
            {'filter': "-1", 'expected': '-1'},
            {'filter': 5.5, 'expected': '5.5'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
            {'filter': {}, 'expected': '{}'},
        ]

        for case in cases:
            filter_param = case.get('filter')
            expected = case.get('expected')
            expected_message = f'`SearchParams(filter={filter_param})` ' + \
                f'should set the `SearchParams.filter` value to `{expected}`.'

            search_params = SearchParams(filter=filter_param)

            self.assertEqual(
                expected, search_params.filter, expected_message)


class SearchResultUnitTest(TestCase):
    def test_should_have_correct_props(self):
        expected = {
            'count': int,
            'current_page': int,
            'current_page_count': int,
            'items_per_page': int,
            'last_page': int,
            'data': List[GenericEntity]
        }

        self.assertDictEqual(expected, SearchResult.__annotations__)

    def test_constructor(self):
        stub = EntityStub(name='name value', age=20)
        search_result = SearchResult(
            data=[stub, stub], count=6, current_page=1, items_per_page=2)

        self.assertListEqual([stub, stub], search_result.data)
        self.assertEqual(1, search_result.current_page)
        self.assertEqual(2, search_result.current_page_count)
        self.assertEqual(2, search_result.items_per_page)
        self.assertEqual(6, search_result.count)
        self.assertEqual(3, search_result.last_page)

    def test_when_data_is_none(self):
        search_result = SearchResult(
            data=None, count=1, current_page=1, items_per_page=1)

        self.assertListEqual([], search_result.data)
        self.assertEqual(0, search_result.current_page_count)

    def test_last_page_when_items_per_page_count_is_greater_than_total_count(self):
        search_result = SearchResult(
            data=[], count=5, current_page=1, items_per_page=10)

        self.assertEqual(1, search_result.last_page)

    def test_last_page_when_items_per_page_count_is_less_than_total_count(self):
        search_result = SearchResult(
            data=[], count=21, current_page=1, items_per_page=10)

        self.assertEqual(3, search_result.last_page)

    def test_to_dict(self):
        stub = EntityStub(name='name value', age=20)
        search_result = SearchResult(
            data=[stub, stub], count=2, current_page=1, items_per_page=2)

        expected = {'count': 2,
                    'items_per_page': 2,
                    'current_page': 1,
                    'current_page_count': 2,
                    'last_page': 1,
                    'data': [stub, stub]}

        self.assertDictEqual(expected, search_result.to_dict())
