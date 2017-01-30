from unittest import TestCase
import numpy as np
import math

from graph.ShortestDistancesFillerMy import ShortestDistancesFillerMy
from graph.ShortestDistancesFillerIGraph import ShortestDistancesFillerIGraph
from space.DistanceMatrix import DistanceMatrix


class TestShortestDistancesFiller(TestCase):

    def test_fill_1(self):
        distance_matrix_with_gaps = DistanceMatrix(np.array([
            [0, 3, 4],
            [3, 0, math.inf],
            [4, math.inf, 0],
        ]))
        distance_matrix_correct_solution = DistanceMatrix(np.array([
            [0, 3, 4],
            [3, 0, 7],
            [4, 7, 0],
        ]))
        sdf = ShortestDistancesFillerMy()
        distance_matrix_result_my = sdf.fill(distance_matrix_with_gaps)
        sdf = ShortestDistancesFillerIGraph()
        distance_matrix_result_igraph = sdf.fill(distance_matrix_with_gaps)

        self.assertEqual(distance_matrix_result_my, distance_matrix_correct_solution)
        self.assertEqual(distance_matrix_result_igraph, distance_matrix_correct_solution)

    def test_fill_2(self):
        distance_matrix_with_gaps = DistanceMatrix(np.array([
            [0, 1, 3, math.inf, math.inf],
            [1, 0, 2, 3, math.inf],
            [3, 2, 0, 1, 3],
            [math.inf, 3, 1, 0, 2],
            [math.inf, math.inf, 3, 2, 0],
        ]))
        distance_matrix_correct_solution = DistanceMatrix(np.array([
            [0, 1, 3, 4, 6],
            [1, 0, 2, 3, 5],
            [3, 2, 0, 1, 3],
            [4, 3, 1, 0, 2],
            [6, 5, 3, 2, 0],
        ]))
        sdf = ShortestDistancesFillerMy()
        distance_matrix_result_my = sdf.fill(distance_matrix_with_gaps)
        sdf = ShortestDistancesFillerIGraph()
        distance_matrix_result_igraph = sdf.fill(distance_matrix_with_gaps)

        self.assertEqual(distance_matrix_result_my, distance_matrix_correct_solution)
        self.assertEqual(distance_matrix_result_igraph, distance_matrix_correct_solution)
