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
        flatten_upper_triangular_matrix = distance_matrix.get_futm()

        correct_flatten_upper_triangular_matrix = [1.0, 2.0, 3.0, 1.0, 2.0, 1.0]
        self.assertEqual(flatten_upper_triangular_matrix, correct_flatten_upper_triangular_matrix)

    def test_get_flatten_upper_triangular_matrix_except_ordered_coordinates(self):
        distance_matrix_base= np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0],
        ])
        distance_matrix = DistanceMatrix(distance_matrix_base)

        coordinates = [[0, 1], [0, 3], [2, 3]]
        flatten_upper_triangular_matrix_wo_coordinates \
            = distance_matrix.get_futm_except_ordered_coordinates(coordinates)

        correct_flatten_upper_triangular_matrix_wo_coordinates = [2.0, 1.0, 2.0]
        self.assertEqual(flatten_upper_triangular_matrix_wo_coordinates,
                         correct_flatten_upper_triangular_matrix_wo_coordinates)

    def test_get_flatten_upper_triangular_matrix_except_ordered_coordinates_wrong_order(self):
        distance_matrix_base= np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0],
        ])
        distance_matrix = DistanceMatrix(distance_matrix_base)

        coordinates = [[0, 3], [0, 1], [2, 3]]
        self.assertRaises(IndexError, distance_matrix.get_futm_except_ordered_coordinates,
                          coordinates)

    def test_get_flatten_upper_triangular_matrix_by_coordinates(self):

        distance_matrix_base = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0],
        ])
        distance_matrix = DistanceMatrix(distance_matrix_base)

        coordinates = [[0, 1], [0, 3], [2, 3]]
        flatten_upper_triangular_matrix_by_coordinates = distance_matrix.get_futm_by_coordinates(
            coordinates)

        correct_flatten_upper_triangular_matrix_by_coordinates = [1.0, 3.0, 1.0]
        self.assertEqual(flatten_upper_triangular_matrix_by_coordinates, correct_flatten_upper_triangular_matrix_by_coordinates)