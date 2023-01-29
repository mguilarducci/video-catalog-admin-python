from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
from unittest import TestCase
from __shared.domain.entities import Entity

from category.domain.entities import Category


class CategoryUnitTest(TestCase):
    def test_should_be_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_should_be_a_subclass_of_entity(self):
        self.assertTrue(issubclass(Category, Entity))

    def test_constructor(self):
        category = Category(name='Movie')

        self.assertEqual('Movie', category.name)
        self.assertIsNone(category.description)
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category2 = Category(
            name='Movie1',
            description='some description',
            is_active=False,
            created_at=created_at
        )

        self.assertEqual('Movie1', category2.name)
        self.assertEqual('some description', category2.description)
        self.assertFalse(category2.is_active)
        self.assertEqual(created_at, category2.created_at)

    def test_if_created_at_is_generated_in_constructor(self):
        category1 = Category(name='Movie 1')
        category2 = Category(name='Movie 2')

        self.assertNotEqual(
            category1.created_at.timestamp(),
            category2.created_at.timestamp()
        )

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = Category(name='test')
            value_object.name = 'fake id'

    def test_should_update_name_and_description(self):
        category = Category(name='name')
        category.update('new name', 'new description')

        self.assertEqual('new name', category.name)
        self.assertEqual('new description', category.description)

    def test_should_activate(self):
        category = Category(name='name', is_active=False)
        category.activate()
        self.assertTrue(category.is_active)

    def test_should_deactivate(self):
        category = Category(name='name', is_active=True)
        category.deactivate()
        self.assertFalse(category.is_active)
