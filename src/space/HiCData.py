import math
import os

import numpy as np

from space.DistanceMatrix import DistanceMatrix
from space.chromosome.Chromosome import Chromosome
from space.gaps_genetrator.GapsGeneratorBase import GapsGeneratorBase


class HiCData:

    def __init__(self, chromosome: Chromosome, not_gaps: list, full: bool=False, name=''):
        self.chromosome = chromosome

        # coordinates of not_gaps sorted by value from smallest
        self.not_gaps = not_gaps

        self.name = name

        self.full = full

    @classmethod
    def from_chromosome_with_gaps_generation(cls, chromosome: Chromosome, gaps_generator: GapsGeneratorBase,
                                             percent_threshold: float):
        if percent_threshold < 0 or percent_threshold > 1:
            raise ValueError('"percent_threshold" should be between 0 and 1.')
        full = (percent_threshold == 0)
        if not full:
            not_gaps = gaps_generator.get_not_gaps(chromosome.distance_matrix.distance_matrix_nparray,
                                                   percent_threshold)
        else:
            not_gaps = None
        return cls(chromosome, not_gaps, full)

    @classmethod
    def from_files(cls, path: str):
        name = os.path.basename(os.path.normpath(path))

        points_path = os.path.join(path, 'points.npy')
        dm_path = os.path.join(path, 'dm.npy')
        if os.path.isfile(points_path):
            points = np.load(points_path)
            chromosome = Chromosome.from_points(points)
        else:
            dm = np.load(dm_path)
            size = dm.shape[0]
            chromosome = Chromosome(np.full((size, 3), 0), size, DistanceMatrix(dm))

        not_gaps_path = os.path.join(path, 'not_gaps.npy')
        not_gaps = np.load(not_gaps_path)

        return cls(chromosome, not_gaps.tolist(), name=name)

    @property
    def size(self):
        return self.chromosome.size

    def get_distance_matrix_with_gaps_old(self) -> DistanceMatrix:
        distance_matrix_with_gaps = np.copy(self.chromosome.distance_matrix.distance_matrix_nparray)
        if self.full:
            return DistanceMatrix(distance_matrix_with_gaps)
        n = distance_matrix_with_gaps.shape[0]
        for x in range(0, n):
            for y in range(x + 1, n):
                if not [x, y] in self.not_gaps:
                    distance_matrix_with_gaps[x, y] = math.inf
                    distance_matrix_with_gaps[y, x] = math.inf
        return DistanceMatrix(distance_matrix_with_gaps)

    def get_distance_matrix_with_gaps(self) -> DistanceMatrix:
        n = self.size
        distance_matrix_with_gaps = np.zeros((n, n))
        distance_matrix_with_gaps.fill(math.inf)
        if self.full:
            return DistanceMatrix(distance_matrix_with_gaps)

        for i in range(0, n):
            distance_matrix_with_gaps[i, i] = 0

        for not_gap in self.not_gaps:
            val = self.chromosome.distance_matrix.distance_matrix_nparray[not_gap[0], not_gap[1]]
            distance_matrix_with_gaps[not_gap[0], not_gap[1]] = val
            distance_matrix_with_gaps[not_gap[1], not_gap[0]] = val

        return DistanceMatrix(distance_matrix_with_gaps)
