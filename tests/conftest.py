import os
from typing import List, Union

from preprocessor.models import Data

try:
    import sys
    sys.path.append(os.getcwd())
except ImportError:
    pass


def create_data_fixture(X: List[str], y: List[Union[str, int]]) -> Data:
    data = {'X': X, 'y': y}
    return Data(**data)
