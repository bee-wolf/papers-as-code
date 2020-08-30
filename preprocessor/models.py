import abc
from typing import List, Union

from pydantic import BaseModel


class Data(BaseModel):
    X: List[str]
    y: List[Union[str, int]]


class Validation:
    def __init__(self, data: Data) -> None:
        self.data = data
        self.description: str
        self.result: bool

    @abc.abstractmethod
    def check(self) -> bool:
        pass

    def run(self):
        self.result = self.check()
