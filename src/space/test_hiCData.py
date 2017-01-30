from unittest import TestCase
import numpy as np
import math

from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData
from space.chromosome.Chromosome import Chromosome


class TestHiCData(TestCase):

    def test_get_distance_matrix_with_gaps(self):
        gaps_generator = OrderedPercentGapsGenerator()
        points = np.array([
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4],
        ])
        chromosome = Chromosome(points)
        hi_c_data = HiCData.from_chromosome_with_gaps_generation(chromosome, gaps_generator, percent_threshold=0.5)

        distance_matrix_with_gaps = hi_c_data.get_distance_matrix_with_gaps()
        dm = distance_matrix_with_gaps.distance_matrix_nparray

        self.assertNotEqual(dm[0][1], math.inf)
        self.assertNotEqual(dm[1][2], math.inf)
        self.assertNotEqual(dm[2][3], math.inf)
        self.assertEqual(dm[0][2], math.inf)
        self.assertEqual(dm[0][3], math.inf)
        self.assertEqual(dm[1][3], math.inf)


    def test_compare_old_and_new_get_distance_matrix_with_gaps(self):
        gaps_generator = OrderedPercentGapsGenerator()
        points = np.array([
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4],
        ])
        chromosome = Chromosome(points)
        hi_c_data = HiCData.from_chromosome_with_gaps_generation(chromosome, gaps_generator, percent_threshold=0.5)

        distance_matrix_with_gaps_old = hi_c_data.get_distance_matrix_with_gaps_old()
        distance_matrix_with_gaps = hi_c_data.get_distance_matrix_with_gaps()

        self.assertTrue(distance_matrix_with_gaps_old, distance_matrix_with_gaps)

