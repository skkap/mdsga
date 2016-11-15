from abc import ABCMeta, abstractmethod
import numpy as np


class GapsGeneratorBase(metaclass=ABCMeta):
    """Base class for various Gap Generators"""

    @abstractmethod
    def get_not_gaps(self, distance_matrix: np.array, percent_threshold: float) -> list:
        pass

