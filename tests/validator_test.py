from typing import Callable, List, Union

import pytest

from preprocessor.validator import Validator


@pytest.fixture()
def custom_validation_non_unique_X():
    return lambda X, y: len(set(X)) > 1


@pytest.mark.parametrize('X, y, expected_result', [
    (['', '', ''], [1, 2, 1], 'passed'),
    (['', '', ''], [1, 1, 1], 'failed'),
])
def test_validator_result(X: List[str], y: List[Union[str, int]], expected_result: str) -> None:
    validator = Validator(X, y)
    validator.validate()
    assert validator.result == expected_result


@pytest.mark.parametrize('X, y, expected_result', [
    (['', '', ''], [1, 2, 1], 'failed'),
    (['1', '2', '3'], [1, 2, 1], 'passed'),
])
def test_custom_validation(X: List[str], y: List[Union[str, int]], expected_result: str,
                           custom_validation_non_unique_X: Callable) -> None:
    validator = Validator(X, y)
    validator.add_custom_validation(custom_validation_non_unique_X)
    validator.validate()
    assert validator.result == expected_result
