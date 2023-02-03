from dataclasses import fields
from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch
from rest_framework.serializers import Serializer

from __shared.domain.validators import DRFValidator, FieldValidatorInterface


class FieldValidatorInterfaceUnitTest(TestCase):
    def test_should_force_an_implementation_of_method_validate(self):
        with self.assertRaises(TypeError) as error:
            # pylint: disable=abstract-class-instantiated
            FieldValidatorInterface()

        expected_message = "Can't instantiate abstract class FieldValidatorInterface " + \
            "with abstract method validate"

        self.assertEqual(expected_message, error.exception.args[0])

    def test_field_values_default(self):
        # sourcery skip: extract-duplicate-method
        class_fields = fields(FieldValidatorInterface)

        errors_field = class_fields[0]
        self.assertEqual('errors', errors_field.name)
        self.assertIsNone(errors_field.default)

        validated_data_field = class_fields[1]
        self.assertEqual('validated_data', validated_data_field.name)
        self.assertIsNone(validated_data_field.default)


# pylint: disable=unused-argument
class DRFValidatorUnitTest(TestCase):
    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(Serializer, 'validated_data', return_value={'field': 'value'},
                  new_callable=PropertyMock)
    def test_should_set_validated_data_when_is_valid_is_true(self,
                                                             mock_validated_data: PropertyMock,
                                                             mock_is_valid: MagicMock):

        validator = DRFValidator()
        validator.validate(Serializer())

        self.assertEqual({'field': 'value'}, validator.validated_data)

    @patch.object(Serializer, 'is_valid', return_value=False)
    @patch.object(Serializer, 'errors', return_value={'field': ['error']},
                  new_callable=PropertyMock)
    def test_should_set_errors_when_is_valid_is_false(self,
                                                      mock_validated_data: PropertyMock,
                                                      mock_is_valid: MagicMock):

        validator = DRFValidator()
        validator.validate(Serializer())

        self.assertEqual({'field': ['error']}, validator.errors)
