from abc import ABCMeta, abstractmethod
from space.DistanceMatrix import DistanceMatrix


class ShortestDistancesFillerBase(metaclass=ABCMeta):

    @abstractmethod
    def fill(self, distance_matrix_with_gaps: DistanceMatrix) -> DistanceMatrix:
        pass