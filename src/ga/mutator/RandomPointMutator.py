import random

from ga.mutator.MutatorBase import MutatorBase
from ga.Organism import Organism


class RandomPointMutator(MutatorBase):

    def __init__(self, frequency_of_mutations: float, lower_bound: float, upper_bound: float):
        self.frequency_of_mutations = frequency_of_mutations
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        pass

    def introduce(self, organism: Organism):
        new_genome = []

        for g in organism.genome:
            r = random.uniform(0, 1)
            if r < self.frequency_of_mutations:
                new_genome.append(self.get_mutated_gene())
            else:
                new_genome.append(g)

        return Organism(new_genome)

    def get_mutated_gene(self):
        new_gene = random.uniform(self.lower_bound, self.upper_bound)
        return new_gene