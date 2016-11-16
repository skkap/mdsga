from abc import ABCMeta, abstractmethod


class FitnessCalculatorBase(metaclass=ABCMeta):
    """Base class for various Fitness Calculators"""

    @abstractmethod
    def calculate(self, flatten_distances_original: list, flatten_distances: list) -> float:
        pass

