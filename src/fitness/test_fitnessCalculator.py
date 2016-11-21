from unittest import TestCase

import numpy as np

from fitness.FitnessCalculator import FitnessCalculator
from space.DistanceMatrix import DistanceMatrix


class TestFitnessCalculator(TestCase):
    def test_compose_distance_matrix(self):
        distance_matrix_base = np.array([
            [0, 1, 2, 3],
            [1, 0, 1, 2],
            [2, 1, 0, 1],
            [3, 2, 1, 0],
        ])
        distance_matrix = DistanceMatrix(distance_matrix_base)
        not_gap_coordinates = [[0, 1], [0, 3], [2, 3]]
        not_gap_values = [1.0, 3.0, 1.0]
        gap_values = [2.0, 1.0, 2.0] # genome

        fitness_calculator = FitnessCalculator(
            score_calculator=None,
            mds=None,
            not_gaps_values=not_gap_values,
            not_gaps_coordinates=not_gap_coordinates,
            size=distance_matrix.size
        )
        result = fitness_calculator.compose_distance_matrix(gap_values)
        self.assertEqual(result, distance_matrix)