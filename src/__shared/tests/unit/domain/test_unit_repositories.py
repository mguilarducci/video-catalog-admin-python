from unittest import TestCase
from __shared.domain.repositories import RepositoryInterface, SearchableRepositoryInterface


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
