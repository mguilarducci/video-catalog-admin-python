from unittest import TestCase
from rest_framework import serializers
from __shared.domain.validators import DRFValidator


# pylint: disable=abstract-method
class SerializerStub(serializers.Serializer):
    char_field = serializers.CharField()
    integer_field = serializers.IntegerField()


class DRFValidatorIntegrationTest(TestCase):
    def test_validate_error(self):
        validator = DRFValidator()
        serializer = SerializerStub(data={})

        is_valid = validator.validate(serializer)

        self.assertFalse(is_valid)
        self.assertDictEqual({'char_field': ['This field is required.'], 'integer_field': [
            'This field is required.']}, validator.errors)

    def test_validate_success(self):
        validator = DRFValidator()
        serializer = SerializerStub(
            data={'char_field': 'value', 'integer_field': 10})

        is_valid = validator.validate(serializer)

        self.assertTrue(is_valid)
        self.assertDictEqual(
            {'char_field': 'value', 'integer_field': 10}, validator.validated_data)
