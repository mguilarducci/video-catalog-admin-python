from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from __shared.domain.entities import Entity
from __shared.domain.exceptions import EntityValidationException
from category.domain.validators import CategoryValidatorFactory


@dataclass(frozen=True, slots=True, kw_only=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=datetime.now
    )

    def __post_init__(self):
        self.validate()

    def update(self, name: str, description: str) -> None:
        self._set('name', name)
        self._set('description', description)
        self.validate()

    def activate(self) -> None:
        self._set('is_active', True)

    def deactivate(self) -> None:
        self._set('is_active', False)

    def validate(self):
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)
