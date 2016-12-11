from fitness.ScoreCalculatorBase import ScoreCalculatorBase
import math


class RMSEScoreCalculator(ScoreCalculatorBase):
    """Calculates score using Root Mean Square Error Method"""

    def __str__(self):
        return 'RMSE'

    def calculate(self, array1: list, array2: list) -> float:
        if len(array1) != len(array2):
            raise ValueError('Size of both arrays should be the same')
        n = len(array1)
        acc = 0
        for i in range(0, n):
            acc += (array1[i] - array2[i]) ** 2
        avg = acc / len(array1)
        rmse = math.sqrt(avg)

        return rmse
