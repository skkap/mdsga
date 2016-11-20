import numpy as np
from sklearn.metrics import euclidean_distances


class DistanceMatrix:

    def __init__(self, distance_matrix_nparray: np.array):
        if distance_matrix_nparray.ndim != 2:
            raise ValueError('"distance_matrix_nparray" should have just two dimensions.')
        if distance_matrix_nparray.shape[0] != distance_matrix_nparray.shape[1]:
            raise ValueError('"distance_matrix_nparray" should be square matrix.')
        if distance_matrix_nparray.shape[0] < 3:
            raise ValueError('"distance_matrix_with_gaps" should be at least 3*3.')

        self.size = distance_matrix_nparray.shape[0]
        self.distance_matrix_nparray = distance_matrix_nparray

    @classmethod
    def from_points(cls, points: np.array):
        if points.ndim != 2:
            raise ValueError('"points" should have two dimensions.')
        if points.shape[0] < 3:
            raise ValueError('"points" should contain at least 3 points.')
        if points.shape[1] != 3:
            raise ValueError('"points" should be X*3 (x,y,z).')
        distance_matrix_nparray = euclidean_distances(points)
        return cls(distance_matrix_nparray)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            equal = np.array_equal(self.distance_matrix_nparray, other.distance_matrix_nparray)
            return equal
        return False

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

    def get_flatten_upper_triangular_matrix_except_coordinates(self, exceptions:list) -> np.array:
        """
        :return: Flat upper triangular part of the matrix without diagonal values and exceptions
        """
        n = self.size
        values = [0] * int(((n * n - n) / 2) - len(exceptions))
        cur = 0
        for x in range(0, n):
            for y in range(x + 1, n):
                if [x, y] in exceptions:
                    continue
                values[cur] = self.distance_matrix_nparray[x, y]
                cur += 1
        return values

    def get_flatten_upper_triangular_matrix_by_coordinates(self, coordinates: list) -> np.array:
        """
        :return: Flat upper triangular part of the matrix by coordinates
        """
        n = self.size
        values = [0] * len(coordinates)
        cur = 0
        for c in coordinates:
            values[cur] = self.distance_matrix_nparray[c[0], c[1]]
            cur += 1
        return values

