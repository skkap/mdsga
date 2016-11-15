from unittest import TestCase
import numpy as np
import math

from graph.ShortestDistancesFiller import ShortestDistancesFiller


class TestShortestDistancesFiller(TestCase):

    def test_fill_1(self):
        distances_with_gaps = np.array([
            [0, 3, 4],
            [3, 0, math.inf],
            [4, math.inf, 0],
        ])
        distances_correct_solution = np.array([
            [0, 3, 4],
            [3, 0, 7],
            [4, 7, 0],
        ])

        sdf = ShortestDistancesFiller()
        distances_sd = sdf.fill(distances_with_gaps)
        self.assertTrue(np.array_equal(distances_correct_solution, distances_sd))

    def test_fill_2(self):
        distances_with_gaps = np.array([
            [0, 1, 3, math.inf, math.inf],
            [1, 0, 2, 3, math.inf],
            [3, 2, 0, 1, 3],
            [math.inf, 3, 1, 0, 2],
            [math.inf, math.inf, 3, 2, 0],
        ])
        distances_correct_solution = np.array([
            [0, 1, 3, 4, 6],
            [1, 0, 2, 3, 5],
            [3, 2, 0, 1, 3],
            [4, 3, 1, 0, 2],
            [6, 5, 3, 2, 0],
        ])

        sdf = ShortestDistancesFiller()
        distances_sd = sdf.fill(distances_with_gaps)
        self.assertTrue(np.array_equal(distances_correct_solution, distances_sd))
