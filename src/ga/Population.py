import math

import numpy as np

from ga.Organism import Organism


class Population:

    def __init__(self, organisms: list):
        self.size = len(organisms)
        if self.size == 0:
            raise RuntimeError('Empty population')
        self.organisms = organisms
        self.genome_size = organisms[0].genome_size

    @classmethod
    def from_file(cls, path: str):
        list_of_genomes = np.load(path)
        organisms = []
        for genome in list_of_genomes:
            organisms.append(Organism(genome.tolist()))
        return cls(organisms)

    def save(self, path: str):
        data = np.zeros((self.size, self.genome_size))
        for i in range(self.size):
            data[i] = self.organisms[i].genome
        np.save(path, np.array(data))

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





