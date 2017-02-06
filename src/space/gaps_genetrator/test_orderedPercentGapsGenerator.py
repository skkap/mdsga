from unittest import TestCase
import numpy as np

from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator


class TestOrderedPercentGapsGenerator(TestCase):

    def test_get_not_gaps_matrix_not_square(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 1, 2, 3, 4],
        ])
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, 0.1)

    def test_get_not_gaps_matrix_with_three_dimensions(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [
                [0, 1],
                [2, 3]
            ],
            [
                [4, 5],
                [6, 7]
            ],
        ])
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, 0.1)

    def test_get_not_gaps_incorrect_percent_threshold(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 1, 2],
            [0, 0, 5],
            [0, 0, 0]
        ])
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, -1)
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, 1.1)

    def test_get_not_gaps_matrix_with_single_element(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0],
        ])
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, 0.1)

    def test_get_not_gaps_two_by_two_matrix(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 1],
            [1, 0]
        ])
        self.assertRaises(ValueError, gaps_generator.get_not_gaps, distance_matrix, 0.1)

    def test_get_not_gaps_correct_input(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 1, 2, 3, 4],
            [0, 0, 5, 6, 7],
            [0, 0, 0, 8, 9],
            [0, 0, 0, 0, 10],
            [0, 0, 0, 0, 0],
        ])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.9)
        self.assertEqual(len(not_gaps), 1)
        self.assertEqual(not_gaps[0], [0, 1])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.5)
        self.assertEqual(len(not_gaps), 5)
        self.assertEqual(not_gaps[0], [0, 1])
        self.assertEqual(not_gaps[1], [0, 2])
        self.assertEqual(not_gaps[2], [0, 3])
        self.assertEqual(not_gaps[3], [0, 4])
        self.assertEqual(not_gaps[4], [1, 2])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.85)
        self.assertEqual(len(not_gaps), 2)
        self.assertEqual(not_gaps[0], [0, 1])
        self.assertEqual(not_gaps[1], [0, 2])

    def test_get_not_gaps_three_by_three_matrix(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 1, 2],
            [0, 0, 3],
            [0, 0, 0]
        ])
        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.1)
        self.assertEqual(len(not_gaps), 3)
        self.assertEqual(not_gaps[0], [0, 1])
        self.assertEqual(not_gaps[1], [0, 2])
        self.assertEqual(not_gaps[2], [1, 2])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.9)
        self.assertEqual(len(not_gaps), 1)
        self.assertEqual(not_gaps[0], [0, 1])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.5)
        self.assertEqual(len(not_gaps), 2)
        self.assertEqual(not_gaps[0], [0, 1])
        self.assertEqual(not_gaps[1], [0, 2])


    def test_get_not_gaps_check_order(self):
        gaps_generator = OrderedPercentGapsGenerator()
        distance_matrix = np.array([
            [0, 3, 2],
            [0, 0, 1],
            [0, 0, 0]
        ])

        not_gaps = gaps_generator.get_not_gaps(distance_matrix, 0.5)
        self.assertEqual(len(not_gaps), 2)
        self.assertEqual(not_gaps[0], [0, 2])
        self.assertEqual(not_gaps[1], [1, 2])