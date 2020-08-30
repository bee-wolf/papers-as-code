from typing import List, Union

import pytest

from conftest import create_data_fixture
from preprocessor.validator import Validator


@pytest.mark.parametrize('X, y, expected_result', [
    (['', '', ''], [1, 2, 1], 'passed'),
    (['', '', ''], [1, 1, 1], 'failed'),
])
def test_validator_result(X: List[str], y: List[Union[str, int]], expected_result: str) -> None:
    validator = Validator(create_data_fixture(X, y))
    validator.validate()
    assert validator.result == expected_result
