from fitness.FitnessCalculatorBase import FitnessCalculatorBase
import math


class RMSEFitnessCalculator(FitnessCalculatorBase):
    """Calculates Fitness using Root Mean Square Error Method"""

    def __str__(self):
        return 'RMSE'

    def calculate(self, flatten_distances_original: list, flatten_distances: list) -> float:
        if len(flatten_distances_original) != len(flatten_distances):
            raise ValueError('Size of both arrays should be the same')
        n = len(flatten_distances_original)
        rmse = 0
        for i in range(0, n):
            rmse += (flatten_distances_original[i] - flatten_distances[i]) ** 2
        rmse /= len(flatten_distances_original)
        rmse = math.sqrt(rmse)

        return rmse
