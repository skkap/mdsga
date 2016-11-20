from unittest import TestCase
import numpy as np

from space.DistanceMatrix import DistanceMatrix


class TestDistanceMatrix(TestCase):
    def test___init__points_2D(self):
        points_2d = np.array([
            [1, 1],
        ])
        with self.assertRaises(ValueError):
            DistanceMatrix(points_2d)

    def test___init__one_point(self):
        point = np.array([
            [1, 1, 1],
        ])
        with self.assertRaises(ValueError):
            DistanceMatrix(point)

    def test___init__(self):
        points = np.array([
            [1, 0, 0],
            [2, 0, 0],
            [3, 0, 0],
            [4, 0, 0],
        ])
        distance_matrix = DistanceMatrix.from_points(points)

        correct_distance_matrix = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0],
        ])
        self.assertEqual(distance_matrix.size, 4)
        self.assertTrue(np.array_equal(distance_matrix.distance_matrix_nparray, correct_distance_matrix))

    def test_get_flatten_upper_triangular_matrix(self):
        points = np.array([
            [1, 0, 0],
            [2, 0, 0],
            [3, 0, 0],
            [4, 0, 0],
        ])
        distance_matrix = DistanceMatrix.from_points(points)
        flatten_upper_triangular_matrix = distance_matrix.get_flatten_upper_triangular_matrix()

        correct_flatten_upper_triangular_matrix = [1.0, 2.0, 3.0, 1.0, 2.0, 1.0]
        self.assertEqual(flatten_upper_triangular_matrix, correct_flatten_upper_triangular_matrix)

    def test_get_flatten_upper_triangular_matrix_except_coordinates(self):
        self.fail()


    def test_get_flatten_upper_triangular_matrix_by_coordinates(self):
        self.fail()