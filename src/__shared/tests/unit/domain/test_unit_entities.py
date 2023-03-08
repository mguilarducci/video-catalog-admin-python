from abc import ABC
from dataclasses import dataclass, is_dataclass
from typing import Optional
from unittest import TestCase

from __shared.domain.entities import Entity
from __shared.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class Stub(Entity):
    prop1: str
    prop2: str
    prop3: Optional[str] = 'default value' # NOSONAR


class EntityUnitTest(TestCase):
    def test_should_be_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_should_be_an_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_constructor_should_set_props_and_id(self):
        entity = Stub(prop1='prop1', prop2='prop2')
        self.assertEqual('prop1', entity.prop1)
        self.assertEqual('prop2', entity.prop2)
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)

    def test_constructor_should_accept_an_id(self):
        entity = Stub(
            unique_entity_id='2d01459a-f739-48d0-a36b-e1cb2a8c72f0', prop1='prop1', prop2='prop2')

        self.assertEqual('2d01459a-f739-48d0-a36b-e1cb2a8c72f0',
                         str(entity.unique_entity_id))

    def test_should_return_id_as_str(self):
        entity = Stub(
            unique_entity_id='2d01459a-f739-48d0-a36b-e1cb2a8c72f0', prop1='prop1', prop2='prop2')
        self.assertEqual('2d01459a-f739-48d0-a36b-e1cb2a8c72f0', entity.id)

    def test_should_return_a_dict(self):
        expected_dict = {
            'id': '2d01459a-f739-48d0-a36b-e1cb2a8c72f0',
            'prop1': 'prop1',
            'prop2': 'prop2',
            'prop3': 'default value'
        }

        entity = Stub(
            unique_entity_id='2d01459a-f739-48d0-a36b-e1cb2a8c72f0', prop1='prop1', prop2='prop2')

        self.assertDictEqual(expected_dict, entity.to_dict())

    def test_set_method(self):
        entity = Stub(prop1='prop1', prop2='prop2')
        entity._set('prop1', 'new value')  # pylint: disable=protected-access
        self.assertEqual('new value', entity.prop1)

    def test_get_default(self):
        result = Stub.get_default('prop1')
        self.assertIsNone(
            result, 'should return None when the field is required')

        result = Stub.get_default('invalid_field')
        self.assertIsNone(
            result, 'should return None when the field is invalid')

        result = Stub.get_default('prop3')
        self.assertEqual('default value', result,
                         'should return the default value')
