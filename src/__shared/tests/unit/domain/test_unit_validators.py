from dataclasses import fields
from unittest import TestCase

from __shared.domain.validators import FieldValidatorInterface


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
