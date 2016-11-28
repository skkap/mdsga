import math

from fitness.ScoreCalculatorBase import ScoreCalculatorBase


class Population:

    def __init__(self, organisms: list):
        self.organisms = organisms
        self.size = len(organisms)

    def get_best_fitness(self):
        best = math.inf
        for o in self.organisms:
            if o.fitness_score < best:
                best = o.fitness_score
        return best





