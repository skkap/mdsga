import numpy as np
import math
import os

from space.gaps_genetrator.GapsGeneratorBase import GapsGeneratorBase
from space.chromosome.Chromosome import Chromosome
from space.DistanceMatrix import DistanceMatrix


class HiCData:

    def __init__(self, chromosome: Chromosome, not_gaps: list, full: bool=False):
        self.chromosome = chromosome
        self.not_gaps = not_gaps
        self.full = full

    @classmethod
    def from_chromosome_with_gaps_generation(cls, chromosome: Chromosome, gaps_generator: GapsGeneratorBase, percent_threshold: float):
        if percent_threshold < 0 or percent_threshold > 1:
            raise ValueError('"percent_threshold" should be between 0 and 1.')
        full = percent_threshold == 0
        if not full:
            not_gaps = gaps_generator.get_not_gaps(chromosome.distance_matrix.distance_matrix_nparray, percent_threshold)
        return cls(chromosome, not_gaps, full)

    @classmethod
    def from_files(cls, directory: str):
        points_path = os.path.join(directory, 'points.txt')
        points = np.loadtxt(points_path)
        chromosome = Chromosome(points)

        not_gaps_path = os.path.join(directory, 'not_gaps.txt')
        not_gaps = np.loadtxt(not_gaps_path)

        return cls(chromosome, not_gaps.tolist())

    @property
    def size(self):
        return self.chromosome.size

    def get_distance_matrix_with_gaps(self) -> DistanceMatrix:
        distance_matrix_with_gaps = np.copy(self.chromosome.distance_matrix.distance_matrix_nparray)
        if self.full:
            return DistanceMatrix(distance_matrix_with_gaps)
        n = distance_matrix_with_gaps.shape[0]
        for x in range(0, n):
            for y in range(x + 1, n):
                is_gap = True
                for not_gap in self.not_gaps:
                    if x == not_gap[0] and y == not_gap[1]:
                        is_gap = False
                        continue
                if is_gap:
                    distance_matrix_with_gaps[x, y] = math.inf
                    distance_matrix_with_gaps[y, x] = math.inf
        return DistanceMatrix(distance_matrix_with_gaps)
