# text-preprocessor

`text-preprocessor` is a Python module for preprocessing textual data prior to downstream NLP classification tasks. The module supports an array of commonly used built-in validations and preprocessing steps as well as support for custom functions.

## Installation

See `requirements.txt` for full list of dependencies.

## Testing

Run `pip install -r requirements_test.txt` for testing dependencies. Launch the test suite using `pytest`.

## Validation Usage

`Validator` can be used to perform data integrity and other checks on the dataset prior to modelling. `X` needs to be an iterable of the strings and `y` is an iterable of the labels.
