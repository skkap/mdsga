from unittest import TestCase
import numpy as np
import math

from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData


class TestHiCData(TestCase):

    def test___init__points_2D(self):
        gaps_generator = OrderedPercentGapsGenerator()
        points_2d = np.array([
            [1, 1],
        ])
        with self.assertRaises(ValueError):
            HiCData(points_2d, gaps_generator, percent_threshold=0.5)

    def test___init__one_point(self):
        gaps_generator = OrderedPercentGapsGenerator()
        point = np.array([
            [1, 1, 1],
        ])
        with self.assertRaises(ValueError):
            HiCData(point, gaps_generator, percent_threshold=0.5)

    def test_get_distance_matrix_with_gaps(self):
        gaps_generator = OrderedPercentGapsGenerator()
        points = np.array([
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4],
        ])

        hi_c_data = HiCData(points, gaps_generator, percent_threshold=0.5)

        distance_matrix_with_gaps = hi_c_data.get_distance_matrix_with_gaps()

        self.assertNotEqual(distance_matrix_with_gaps[0][1], math.inf)
        self.assertNotEqual(distance_matrix_with_gaps[1][2], math.inf)
        self.assertNotEqual(distance_matrix_with_gaps[2][3], math.inf)

        self.assertEqual(distance_matrix_with_gaps[0][2], math.inf)
        self.assertEqual(distance_matrix_with_gaps[0][3], math.inf)
        self.assertEqual(distance_matrix_with_gaps[1][3], math.inf)

