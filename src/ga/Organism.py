import math
import numpy as np


class Organism:

    # TODO: change to numpy
    def __init__(self, genome: list):
        self.genome = genome
        self.genome_size = len(genome)
        self.fitness_score = math.inf

    @classmethod
    def from_file(cls, path: str):
        genome = np.load(path)
        return cls(genome.tolist())

    def save(self, path: str):
        np.save(path, np.array(self.genome))
