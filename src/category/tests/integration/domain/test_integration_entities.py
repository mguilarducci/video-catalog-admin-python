from unittest import TestCase
from __shared.domain.exceptions import EntityValidationException
from category.domain.entities import Category


class CategoryIntegrationTest(TestCase):
    error_messages = {
        'required': 'This field is required.',
        'not_null': 'This field may not be null.',
        'not_blank': 'This field may not be blank.',
        'max_length': 'Ensure this field has no more than 255 characters.',
        'invalid_boolean': 'Must be a valid boolean.',
        'invalid_datetime': 'Datetime has wrong format. Use one of these formats instead: ' +
        'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
    }

    def test_create_category_with_invalid_names(self):
        invalid_inputs = [
            {'data': {'name': None}, 'expected': self.error_messages.get(
                'not_null'), 'message': 'name should not be None'},
            {'data': {'name': ''}, 'expected': self.error_messages.get(
                'not_blank'), 'message': 'name should not be blank'},
            {'data': {'name': 'x'*256}, 'expected': self.error_messages.get(
                'max_length'), 'message': 'name should not have more than 255 chars'},
        ]

        for invalid_input in invalid_inputs:
            with self.assertRaises(EntityValidationException) as error:
                Category(**invalid_input.get('data'))
                self.assertEqual(invalid_input.get('expected'),
                                 error.exception.errors.get('name').pop(),
                                 invalid_input.get('message'))

    def test_update_category_with_valid_args(self):
        category_name = 'category name'
        category = Category(name=category_name)

        try:
            category.update(category_name, None)  # NOSONAR
            category.update(category_name, '')
            category.update(category_name, 'description')
        except EntityValidationException as exception:
            self.fail(exception.args[0])
