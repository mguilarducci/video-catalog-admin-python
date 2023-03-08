from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from category.domain.entities import Category


@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str  # pylint: disable=invalid-name
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


@dataclass(slots=True, frozen=True)
class CategoryOutputMapper:
    @staticmethod
    def to_output(category: Category):
        return CategoryOutput(id=category.id,
                              name=category.name,
                              description=category.description,
                              is_active=category.is_active,
                              created_at=category.created_at)
