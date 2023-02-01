from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar


ErrorsField = Dict[str, List[str]]
ValidatedDataField = TypeVar('ValidatedDataField')


@dataclass(slots=True)
class FieldValidatorInterface(ABC, Generic[ValidatedDataField]):
    errors: ErrorsField = None
    validated_data: ValidatedDataField = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()
