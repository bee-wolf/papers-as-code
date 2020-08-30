import abc
from typing import List, Union


class Validation:
    def __init__(self, X: List[str], y: List[Union[str, int]]) -> None:
        self.X = X
        self.y = y
        self.message: str
        self.result: bool

    @abc.abstractmethod
    def check(self) -> bool:
        pass

    def run(self):
        self.result = self.check()
