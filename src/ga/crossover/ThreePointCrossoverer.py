import random

from ga.crossover.CrossovererBase import CrossoverrerBase
from ga.Organism import Organism


class ThreePointCrossoverer(CrossoverrerBase):

    def crossover(self, organism1: Organism, organism2: Organism):

        if organism1.genome_size != organism1.genome_size:
            raise ValueError('Genome of organisms should be same size')

        genome_size = organism1.genome_size

        one_third_point = int(genome_size / 3)

        two_third_point = int(genome_size / 3) * 2

        crossover_point1 = random.randint(0, one_third_point)

        crossover_point2 = random.randint(one_third_point, two_third_point)

        crossover_point3 = random.randint(two_third_point, genome_size)

        new_genome = []
        for i in range(genome_size):
            if i < crossover_point1:
                new_genome.append(organism1.genome[i])
            elif crossover_point1 <= i < crossover_point2:
                new_genome.append(organism2.genome[i])
            elif crossover_point2 <= i < crossover_point3:
                new_genome.append(organism1.genome[i])
            else:
                new_genome.append(organism2.genome[i])

        return Organism(new_genome)

