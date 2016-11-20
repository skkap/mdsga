from abc import ABCMeta, abstractmethod


class ScoreCalculatorBase(metaclass=ABCMeta):
    """Base class for various Score Calculators"""

    @abstractmethod
    def calculate(self, flatten_distances_original: list, flatten_distances: list) -> float:
        pass