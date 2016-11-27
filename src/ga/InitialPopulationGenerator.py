import random

from ga.Organism import Organism
from ga.Population import Population


class InitialPopulationGenerator:

    def generate(self, original_organism: Organism, population_size: int):

        organisms = []

        for i in range(0, population_size):
            new_organism = self.generate_organism(original_organism)
            organisms.append(new_organism)

        population = Population(organisms)
        return population

    def generate_organism(self, original_organism: Organism):
        new_genome = []
        for gene in original_organism.genome:
            rand = random.randint(0, int((gene) / 2))
            new_genome.append(gene - rand)
        return Organism(new_genome)