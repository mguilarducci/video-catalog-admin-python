from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from rest_framework.serializers import Serializer
from django.conf import settings


if not settings.configured:
    settings.configure(USE_I18N=False)


ErrorsField = Dict[str, List[str]]
ValidatedDataField = TypeVar('ValidatedDataField')


@dataclass(slots=True)
class FieldValidatorInterface(ABC, Generic[ValidatedDataField]):
    errors: ErrorsField = None
    validated_data: ValidatedDataField = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(FieldValidatorInterface[ValidatedDataField], ABC):
    def validate(self, data: Serializer) -> bool:
        if data.is_valid():
            self.validated_data = dict(data.validated_data)
            return True

        self.errors = {field: [str(error) for error in errors]
                       for field, errors in data.errors.items()}

        return False
