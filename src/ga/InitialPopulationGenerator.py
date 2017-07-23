import random

from ga.Organism import Organism
from ga.Population import Population


class InitialPopulationGenerator:

    def generate(self, original_organism: Organism, population_size: int, add_original_organism: bool=False):

        organisms = []

        if add_original_organism:
            organisms.append(original_organism)

        while len(organisms) < population_size:
            new_organism = self.generate_organism(original_organism)
            organisms.append(new_organism)

        population = Population(organisms)
        return population

    def generate_organism(self, original_organism: Organism):
        new_genome = []
        for gene in original_organism.genome:
            rand = random.uniform(0, gene / 3)
            new_genome.append(gene - rand)
        return Organism(new_genome)
