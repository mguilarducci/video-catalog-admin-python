from typing import Dict
from rest_framework import serializers
from __shared.domain.validators import DRFValidator


# pylint: disable=abstract-method
class CategoryValidationRules(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):
    def validate(self, data: Dict) -> bool:
        validation_rules_data = data if data is not None else {}
        validation_rules = CategoryValidationRules(data=validation_rules_data)

        return super().validate(validation_rules)


class CategoryValidatorFactory:
    @staticmethod
    def create():
        return CategoryValidator()
