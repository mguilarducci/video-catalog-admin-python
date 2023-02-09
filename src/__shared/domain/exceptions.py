from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from __shared.domain.validators import ErrorsField


class InvalidUniqueEntityIdValueException(Exception):
    pass


class EntityValidationException(Exception):
    errors: 'ErrorsField'

    def __init__(self, errors: 'ErrorsField') -> None:
        self.errors = errors
        super().__init__('Entity Validation Error')
