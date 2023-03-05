from abc import ABC
from __shared.domain.repositories import (
    SearchParams as BaseSearchParams,
    SearchResult as BaseSearchResult,
    SearchableRepositoryInterface)
from category.domain.entities import Category


class _SearchParams(BaseSearchParams): # pylint: disable=too-few-public-methods
    pass


class _SearchResult(BaseSearchResult): # pylint: disable=too-few-public-methods
    pass


class CategoryRepositoryInterface(SearchableRepositoryInterface[Category,
                                                                _SearchParams,
                                                                _SearchResult],
                                  ABC):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
