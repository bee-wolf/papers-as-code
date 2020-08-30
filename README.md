# text-preprocessor

`text-preprocessor` is a Python module for preprocessing textual data prior to downstream NLP classification tasks. The module supports an array of commonly used built-in validations and preprocessing steps as well as support for custom functions.

## Installation

See `requirements.txt` for full list of dependencies.

## Testing

Run `pip install -r requirements_test.txt` for testing dependencies. Launch the test suite using `pytest`.

## Validation Usage

`Validator` can be used to perform data integrity and other checks on the dataset prior to modelling. `X` needs to be an iterable of the strings and `y` is an iterable of the labels.

```
import numpy as np
from preprocessor.validator import Validator

X = np.array(['first sentence', 'second sentence', 'last one'])
y = np.ones(3)

validator = Validator(X, y)
validator.validate()
```

## Adding a Custom Validator

Say that you have a custom function you would like to add to the validation pipeline. Restructure it to provide a boolean response (True = passed validation checks, False = flag for review). The function must accept an `X` and `y`.

```
def my_custom_validator(X, y) -> bool:
    return len(X) == len(y)


validator.add_custom_validation(my_custom_validator, message='custom validator failed', severity='high')
validator.validate()
```
