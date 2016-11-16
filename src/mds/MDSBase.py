from abc import ABCMeta, abstractmethod

from space.DistanceMatrix import DistanceMatrix
from space.chromosome.Chromosome import Chromosome


class MDSBase(metaclass=ABCMeta):
    """Base class for various MDS implementations"""

    @abstractmethod
    def run(self, distance_matrix: DistanceMatrix) -> Chromosome:
        """Returns reconstructed coordinates from distance matrix"""
        pass


