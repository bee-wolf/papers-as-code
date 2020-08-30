import abc
from typing import List, Union


class Validation:
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        self.X = X
        self.y = y
        self.result: bool
        self.message: str
        self.severity: str  # LOW, MEDIUM, HIGH

    @abc.abstractmethod
    def get_message(self) -> str:
        pass

    @abc.abstractmethod
    def check(self) -> bool:
        pass

    def run(self):
        self.result = self.check()
        self.message = self.get_message()
