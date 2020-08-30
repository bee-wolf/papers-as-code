import inspect
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from preprocessor.models import Validation


def create_custom_validation(custom_check: Callable) -> Validation:
    def custom_init(self, X, y):
        self.X = X
        self.y = y

    def custom_message(self):
        return 'Custom Validation Step'
    CustomValidation = type('CustomValidation', (Validation,),
                            {'__init__': custom_init,
                             'check': lambda self: custom_check(self.X, self.y),
                             'get_message': custom_message})
    return CustomValidation


class CheckMultipleClasses(Validation):
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        super().__init__(X=X, y=y)
        self.severity = 'high'

    def check(self) -> bool:
        return len(np.unique(self.y)) > 1

    def get_message(self) -> str:
        return 'Single class detected'


class CheckDuplicateRecords(Validation):
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        super().__init__(X=X, y=y)
        self.severity = 'low'

    def check(self) -> bool:
        return len(np.unique(self.X)) == len(self.X)

    def get_message(self) -> str:
        return 'At least one data point is duplicated; consider removing duplicates'


class CheckNonASCIICharacters(Validation):
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        super().__init__(X=X, y=y)
        self.severity = 'low'
        self.non_unicode: List[str] = []

    def check(self) -> bool:
        for obs in self.X:
            self.non_unicode += [c for c in obs if ord(c) >= 128]
        return set(self.non_unicode) == set()

    def get_message(self) -> str:
        return f'Non-ASCII characters detected (may interfere with pre-trained embeddings): {set(self.non_unicode)}'  # noqa


class Validator:
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        self.X = X
        self.y = y
        self.custom_validations: List[Tuple[str, Validation]] = []
        self.output: Dict[str, Dict[str, str]] = {}
        self.result: str

    def _is_validation(self, obj: Any) -> bool:
        return inspect.isclass(obj) and issubclass(obj, Validation) and obj.__name__.startswith('Check')

    def _get_failed_validation_details(self, validation: Validation) -> Dict[str, str]:
        return {
            'message': getattr(validation, 'message', 'N/A - custom validation'),
            'severity': getattr(validation, 'severity', 'N/A - custom validation')
        }

    def add_custom_validation(self,
                              validation: Callable,
                              message: Optional[str] = None,
                              severity: Optional[str] = None) -> None:
        custom_validation = create_custom_validation(validation)
        if message:
            custom_validation.message = message
        if severity:
            custom_validation.severity = severity
        self.custom_validations.append((validation.__name__, custom_validation))

    def validate(self) -> None:
        validations = inspect.getmembers(sys.modules[__name__], self._is_validation) + self.custom_validations
        for name, validation in validations:
            data_validation = validation(self.X, self.y)
            data_validation.run()
            if data_validation.result is False:
                self.output[name] = self._get_failed_validation_details(data_validation)
        self.result = 'passed' if self.output == {} else 'failed'
