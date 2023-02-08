from datetime import datetime
from unittest import TestCase
from __shared.domain.validators import FieldValidatorInterface

from category.domain.validators import CategoryValidator, CategoryValidatorFactory


class CategoryValidatorFactoryUnitTest(TestCase):
    def test_should_return_category_validator(self):
        validator = CategoryValidatorFactory.create()
        self.assertIsInstance(validator, CategoryValidator)

    def test_should_return_field_validator_interface_subclass(self):
        validator = CategoryValidatorFactory.create()
        self.assertTrue(issubclass(
            validator.__class__, FieldValidatorInterface))


class CategoryValidatorUnitTest(TestCase):
    error_messages = {
        'required': 'This field is required.',
        'not_null': 'This field may not be null.',
        'not_blank': 'This field may not be blank.',
        'max_length': 'Ensure this field has no more than 255 characters.',
        'invalid_boolean': 'Must be a valid boolean.',
        'invalid_datetime': 'Datetime has wrong format. Use one of these formats instead: ' +
        'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
    }

    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidator()
        return super().setUp()

    def test_should_not_validate_name_with_invalid_values(self):
        invalid_inputs = [
            {'data': None, 'expected': self.error_messages.get(
                'required'), 'message': 'object data should not be None'},
            {'data': {}, 'expected': self.error_messages.get(
                'required'), 'message': 'object data should not be empty'},
            {'data': {'name': None}, 'expected': self.error_messages.get(
                'not_null'), 'message': 'name should not be None'},
            {'data': {'name': ''}, 'expected': self.error_messages.get(
                'not_blank'), 'message': 'name should not be blank'},
            {'data': {'name': 'x'*256}, 'expected': self.error_messages.get(
                'max_length'), 'message': 'name should not have more than 255 chars'},
        ]

        for invalid_input in invalid_inputs:
            is_valid = self.validator.validate(invalid_input.get('data'))
            self.assertFalse(is_valid)
            self.assertEqual(invalid_input.get('expected'),
                             self.validator.errors.get('name').pop(),
                             invalid_input.get('message'))

    def test_should_validate_name_with_values(self):
        # sourcery skip: class-extract-method, extract-duplicate-method
        data = {'name': 'name value'}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'name should be valid with correct value')

        data = {'name': 'n'}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'name should be valid with 1 char')

        data = {'name': 'n'*255}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'name should be valid with 255 chars')

    def test_should_validate_description_with_values(self):
        # sourcery skip: extract-duplicate-method
        data = {'name': 'name', 'description': None}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'description can be None')

        data = {'name': 'valid name', 'description': ''}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'description can be blank')

        data = {'name': 'valid name'}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'description can be empty')

    def test_should_not_validate_is_active_with_invalid_values(self):
        data = {'name': 'name', 'is_active': None}
        is_valid = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(self.error_messages.get('not_null'),
                         self.validator.errors.get('is_active').pop(),
                         'is_active should not be none')

        data = {'name': 'name', 'is_active': ''}
        is_valid = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(self.error_messages.get('invalid_boolean'),
                         self.validator.errors.get('is_active').pop(),
                         'is_active should not be empty')

    def test_should_validate_is_active_with_values(self):
        # sourcery skip: extract-duplicate-method
        data = {'name': 'name', 'is_active': True}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'is_active can be True')

        data = {'name': 'name', 'is_active': False}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'is_active can be False')

        data = {'name': 'name'}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'is_active can be empty')

    def test_should_not_validate_created_at_with_invalid_values(self):
        data = {'name': 'name', 'created_at': None}
        is_valid = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(self.error_messages.get('not_null'),
                         self.validator.errors.get('created_at').pop(),
                         'created_at should not be none')

        data = {'name': 'name', 'created_at': ''}
        is_valid = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(self.error_messages.get('invalid_datetime'),
                         self.validator.errors.get('created_at').pop(),
                         'created_at should not be blank')

    def test_should_validate_created_at_with_valid_values(self):
        # sourcery skip: extract-duplicate-method
        data = {'name': 'name'}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'created_at can be empty')

        data = {'name': 'name', 'created_at': datetime.now()}
        is_valid = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertDictEqual(data, self.validator.validated_data,
                             'created_at can be a datetime')
