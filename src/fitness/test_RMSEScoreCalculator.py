from unittest import TestCase

from fitness.RMSEScoreCalculator import RMSEScoreCalculator


class TestRMSEScoreCalculator(TestCase):
    def test_calculate_equal(self):
        array1 = [1, 1, 1, 1]
        rmse_score_calculator = RMSEScoreCalculator()
        fitness = rmse_score_calculator.calculate(array1, array1)
        self.assertEqual(fitness, 0)

    def test_calculate_different(self):
        array1 = [1, 1, 1, 1]
        array2 = [1, 1, 1, 2]
        rmse_score_calculator = RMSEScoreCalculator()
        fitness = rmse_score_calculator.calculate(array1, array2)
        self.assertEqual(fitness, 0.5)

    def test_calculate_different2(self):
        array1 = [1, 5, 1, 5]
        array2 = [1, 1, 1, 2]
        rmse_score_calculator = RMSEScoreCalculator()
        fitness = rmse_score_calculator.calculate(array1, array2)
        self.assertAlmostEqual(fitness, 2.5)
