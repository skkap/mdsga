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

    def get_worst_fitness(self):
        worst = 0
        for o in self.organisms:
            if o.fitness_score > worst:
                worst = o.fitness_score
        return worst

    def get_average_fitness(self):
        total = 0
        for o in self.organisms:
            total += o.fitness_score
        return total / self.size

    def get_best_organism(self):
        best = math.inf
        best_i = 0
        for i, o in enumerate(self.organisms):
            if o.fitness_score < best:
                best = o.fitness_score
                best_i = i
        return self.organisms[best_i]





