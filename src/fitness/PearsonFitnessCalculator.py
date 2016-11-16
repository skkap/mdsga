from fitness.FitnessCalculatorBase import FitnessCalculatorBase
from scipy import stats


class PearsonFitnessCalculator(FitnessCalculatorBase):
    """Calculates Fitness using Pearson product-moment correlation coefficient"""

    def __str__(self):
        return 'Pearson'

    def calculate(self, flatten_distances_original: list, flatten_distances: list) -> float:
        pearson_result = stats.pearsonr(flatten_distances_original, flatten_distances)
        return pearson_result[0]
