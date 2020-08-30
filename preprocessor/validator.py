import inspect
import sys
from typing import Any, Callable, Dict, List, Tuple, Union

from preprocessor.models import Validation


def create_custom_validation(custom_check: Callable) -> Validation:
    def custom_init(self, X, y):
        self.X = X
        self.y = y
    CustomValidation = type('CustomValidation', (Validation,),
                            {'__init__': custom_init,
                             'check': lambda self: custom_check(self.X, self.y)})
    return CustomValidation


class CheckMultipleClasses(Validation):
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        super().__init__(X=X, y=y)
        self.message = 'Single class detected'

    def check(self) -> bool:
        return len(set(self.y)) > 1


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
            'message': validation.message if hasattr(validation, 'message') else 'N/A',
        }

    def add_custom_validation(self, validation: Callable) -> None:
        custom_validation = create_custom_validation(validation)
        self.custom_validations.append((validation.__name__, custom_validation))

    def validate(self) -> None:
        validations = inspect.getmembers(sys.modules[__name__], self._is_validation) + self.custom_validations
        for name, validation in validations:
            data_validation = validation(self.X, self.y)
            data_validation.run()
            if not data_validation.result:
                self.output[name] = self._get_failed_validation_details(data_validation)
        self.result = 'passed' if self.output == {} else 'failed'
