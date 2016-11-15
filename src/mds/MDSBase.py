from abc import ABCMeta, abstractmethod
import numpy as np

class MDSBase(metaclass=ABCMeta):
    """Base class for various MDS implementations"""

    @abstractmethod
    def run(self, distance_matrix: np.array) -> np.array:
        """Returns reconstructed coordinates from distance matrix"""
        pass


