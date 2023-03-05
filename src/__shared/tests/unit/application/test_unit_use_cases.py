from unittest import TestCase

from __shared.application.use_cases import UseCase


class UseCaseUnitTest(TestCase):
    def test_should_implements_execute_method(self):
        with self.assertRaises(TypeError) as error:
            UseCase()  # pylint: disable=abstract-class-instantiated

        message = "Can't instantiate abstract class UseCase with abstract method execute"
        self.assertEqual(message, error.exception.args[0])
