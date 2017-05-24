import os

from ga.Organism import Organism
from ga.Population import Population
from space.HiCData import HiCData


class Sample:
    def __init__(self,  path: str):
        initial_organism_path = os.path.join(path, 'initial_organism.npy')
        if os.path.isfile(initial_organism_path):
            self.initial_organism = Organism.from_file(initial_organism_path)
        else:
            self.initial_organism = None

        initial_population_path = os.path.join(path, 'initial_population.npy')
        if os.path.isfile(initial_population_path):
            self.initial_population = Population.from_file(initial_population_path)
        else:
            self.initial_population = None

        self.hic_data = HiCData.from_files(path)
