import random

from ga.mutator.MutatorBase import MutatorBase
from ga.Organism import Organism


class RandomPointMutator(MutatorBase):

    def __init__(self, frequency_of_mutations: float, initial_organism: Organism, divider: int):
        self.frequency_of_mutations = frequency_of_mutations
        self.initial_organism = initial_organism
        self.divider = divider

        pass

    def introduce(self, organism: Organism):
        new_genome = []

        for i, g in enumerate(organism.genome):
            r = random.uniform(0, 1)
            if r < self.frequency_of_mutations:
                initial_gene = self.initial_organism.genome[i]
                rand = random.uniform(0, int(initial_gene / self.divider))
                new_genome.append(initial_gene - rand)
            else:
                new_genome.append(g)

        return Organism(new_genome)
