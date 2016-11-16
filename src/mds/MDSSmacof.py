from mds.MDSBase import MDSBase
from sklearn import manifold
import numpy as np

from space.DistanceMatrix import DistanceMatrix
from space.chromosome.Chromosome import Chromosome


class MDSSmacof(MDSBase):
    """MDS implementation in sklearn.manifold.MDS, iterative metric SMACOF algorithm"""

    def __str__(self):
        return 'MDS SMACOF algorithm'

    def __init__(self, dimensions=3, max_iter=3000, eps=1e-9):
        self.calculator = manifold.MDS(n_components=dimensions, max_iter=max_iter, eps=eps,
                                       dissimilarity="precomputed", n_jobs=1)

    def run(self, distance_matrix: DistanceMatrix) -> Chromosome:
        result_points = self.calculator.fit(distance_matrix.distance_matrix_nparray).embedding_
        result_chromosome = Chromosome(result_points)
        return result_chromosome
