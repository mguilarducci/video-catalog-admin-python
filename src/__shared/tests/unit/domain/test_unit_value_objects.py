from abc import ABC
from unittest import TestCase
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import uuid
from __shared.domain.exceptions import InvalidUniqueEntityIdValueException
from __shared.domain.value_objects import UniqueEntityId, ValueObject


@dataclass(frozen=True)
class Stub1(ValueObject):
    prop: str


@dataclass(frozen=True)
class Stub2(ValueObject):
    prop1: str
    prop2: str


class ValueObjectBaseUnitTest(TestCase):
    def test_should_be_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_should_be_an_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init(self):
        obj1 = Stub1(prop='prop1')
        self.assertEqual('prop1', obj1.prop)

        obj2 = Stub2(prop1='prop1', prop2='prop2')
        self.assertEqual('prop1', obj2.prop1)
        self.assertEqual('prop2', obj2.prop2)

    def test_should_be_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            obj = Stub1(prop='prop')
            obj.prop = 'error!'

    def test_to_str_should_return_prop_as_string_when_has_only_one_property(self):
        obj = Stub1('prop value')
        self.assertEqual('prop value', str(obj))

    def test_to_str_should_return_json_as_string_when_has_more_than_one_property(self):
        obj = Stub2(prop1='one', prop2='two')
        self.assertEqual('{"prop1": "one", "prop2": "two"}', str(obj))


# pylint: disable=protected-access
class UniqueEntityIdUnitTest(TestCase):
    def test_should_be_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_should_be_a_value_object(self):
        self.assertTrue(issubclass(UniqueEntityId, ValueObject))

    def test_should_throw_an_exception_when_id_arg_is_invalid(self):
        with self.assertRaises(InvalidUniqueEntityIdValueException):
            UniqueEntityId('invalid id')

    def test_should_accept_a_valid_id_passed_in_constructor(self):
        obj = UniqueEntityId('2d01459a-f739-48d0-a36b-e1cb2a8c72f0')
        self.assertEqual(obj._id, '2d01459a-f739-48d0-a36b-e1cb2a8c72f0')

    def test_should_create_an_id_when_nothing_is_passed_in_constructor(self):
        obj = UniqueEntityId()
        self.assertIsNotNone(obj._id)
        uuid.UUID(obj._id)

    def test_should_be_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            obj = UniqueEntityId()
            obj._id = 'id'

    def test_to_str_should_return_id_as_str(self):
        obj = UniqueEntityId('2d01459a-f739-48d0-a36b-e1cb2a8c72f0')
        self.assertEqual('2d01459a-f739-48d0-a36b-e1cb2a8c72f0', str(obj))
