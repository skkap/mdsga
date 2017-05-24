from unittest import TestCase

from fitness.RMSEScoreCalculator import RMSEScoreCalculator
from ga.Organism import Organism
from ga.crossover.MiddlePointCrossoverer import MiddlePointCrossoverer


class TestMiddlePointCrossoverre(TestCase):
    def test_10(self):
        organism1 = Organism([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        organism2 = Organism([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        crossoverer = MiddlePointCrossoverer()
        result = crossoverer.crossover(organism1, organism2)
        self.assertEqual(result.genome, [1, 1, 1, 1, 1, 2, 2, 2, 2, 2])

    def test_5(self):
        organism1 = Organism([1, 1, 1, 1, 1])
        organism2 = Organism([2, 2, 2, 2, 2])
        crossoverer = MiddlePointCrossoverer()
        result = crossoverer.crossover(organism1, organism2)
        self.assertEqual(result.genome, [1, 1, 2, 2, 2])

