import numpy as np
import math
from sklearn.metrics import euclidean_distances

from space.gaps_genetrator.GapsGeneratorBase import GapsGeneratorBase


class HiCData:

    def __init__(self, points: np.array, gaps_generator: GapsGeneratorBase, percent_threshold: float):

        if points.ndim != 2:
            raise ValueError('"points" should have two dimensions.')
        if points.shape[0] < 3:
            raise ValueError('"points" should contain at least 3 points.')
        if points.shape[1] != 3:
            raise ValueError('"points" should be X*3 (x,y,z).')
        if percent_threshold < 0 or percent_threshold > 1:
            raise ValueError('"percent_threshold" should be between 0 and 1.')

        self.full_distance_matrix = euclidean_distances(points)
        self.not_gaps = gaps_generator.get_not_gaps(self.full_distance_matrix, percent_threshold)

    def get_distance_matrix_with_gaps(self) -> np.array:
        distance_matrix_with_gaps = np.copy(self.full_distance_matrix)
        n = distance_matrix_with_gaps.shape[0]
        for x in range(0, n):
            for y in range(x + 1, n):
                is_gap = True
                for not_gap in self.not_gaps:
                    if x == not_gap[0] and y == not_gap[1]:
                        is_gap = False
                        continue
                if is_gap:
                    distance_matrix_with_gaps[x, y] = math.inf
                    distance_matrix_with_gaps[y, x] = math.inf
        return distance_matrix_with_gaps
