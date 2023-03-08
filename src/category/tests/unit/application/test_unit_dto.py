from unittest import TestCase

from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category


class CategoryOutputMapperUnitTest(TestCase):
    def test_to_output_behavior(self):
        category = Category(name='name')

        category_output_expected = CategoryOutput(id=category.id,
                                                  name=category.name,
                                                  description=category.description,
                                                  is_active=category.is_active,
                                                  created_at=category.created_at)

        output = CategoryOutputMapper.to_output(category)
        self.assertEqual(category_output_expected, output)
