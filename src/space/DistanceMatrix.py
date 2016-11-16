import numpy as np
from sklearn.metrics import euclidean_distances


class DistanceMatrix:

    def __init__(self, points: np.array):
        self.size = points.shape[0]
        self.distance_matrix_nparray = euclidean_distances(points)

    def get_flatten_upper_triangular_matrix(self) -> np.array:
        """
        :return: Flat upper triangular part of the matrix without diagonal values
        """
        n = self.size
        values = [0] * int((n * n - n) / 2)
        cur = 0
        for x in range(0, n):
            for y in range(x + 1, n):
                values[cur] = self.distance_matrix_nparray[x, y]
                cur += 1
        return values

