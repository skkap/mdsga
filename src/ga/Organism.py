import math

class Organism:

    def __init__(self, genome: list):
        self.genome = genome
        self.genome_size = len(genome)
        self.fitness_score = math.inf



