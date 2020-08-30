import inspect
import sys
from typing import Any, Dict, List, Tuple

from preprocessor.models import Data, Validation


class CheckMultipleClasses(Validation):
    def __init__(self, data: Data) -> None:
        super().__init__(data=data)
        self.description = 'Single class detected'

    def check(self) -> bool:
        return len(set(self.data.y)) > 1


class Validator:
    def __init__(self, data: Data) -> None:
        self.data = data
        self.custom_validations: List[Tuple[str, Validation]] = []
        self.output: Dict[str, Dict[str, str]] = {}
        self.result: str

    def _is_validation(self, obj: Any) -> bool:
        return inspect.isclass(obj) and issubclass(obj, Validation) and obj.__name__.startswith('Check')

    def _get_failed_validation_details(self, validation: Validation) -> Dict[str, str]:
        return {
            'description': validation.description,
        }

    def add_custom_validation(self, validations: List[Validation]) -> None:
        # TODO: regular callables to be transformed into custom validations
        for validation in validations:
            self.custom_validations.append((validation.__name__, validation))

    def validate(self) -> None:
        validations = inspect.getmembers(sys.modules[__name__], self._is_validation) + self.custom_validations
        for name, validation in validations:
            data_validation = validation(self.data)
            data_validation.run()
            if not data_validation.result:
                self.output[name] = self._get_failed_validation_details(data_validation)
        self.result = 'passed' if self.output == {} else 'failed'
