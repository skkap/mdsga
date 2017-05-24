from ga.crossover.CrossovererBase import CrossoverrerBase
from ga.Organism import Organism


class MiddlePointCrossoverer(CrossoverrerBase):

    def crossover(self, organism1: Organism, organism2: Organism):

        if organism1.genome_size != organism1.genome_size:
            raise ValueError('Genome of organisms should be same size')

        genome_size = organism1.genome_size

        crossover_point = int(genome_size / 2)

        new_genome = []
        for i in range(genome_size):
            if i < crossover_point:
                new_genome.append(organism1.genome[i])
            else:
                new_genome.append(organism2.genome[i])

        return Organism(new_genome)

