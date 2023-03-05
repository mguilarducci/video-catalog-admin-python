from abc import ABC, abstractmethod
from typing import Generic, TypeVar

UseCaseInput = TypeVar('UseCaseInput')
UseCaseOutput = TypeVar('UseCaseOutput')


class UseCase(Generic[UseCaseInput, UseCaseOutput], ABC):
    @abstractmethod
    def execute(self, input_params: UseCaseInput) -> UseCaseOutput:
        raise NotImplementedError()
