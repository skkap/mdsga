from mds.MDSBase import MDSBase
from sklearn import decomposition
import numpy as np

from space.DistanceMatrix import DistanceMatrix
from space.chromosome.Chromosome import Chromosome


class MDSTorgerson(MDSBase):
    """MDS implementation in sklearn.decomposition.PCA, determinated Principal component analysis (PCA),
     traditional Torgerson algorithm"""

    def __str__(self):
        return 'MDS Torgerson algorithm'

    def __init__(self, dimensions=3):
        self.calculator = decomposition.PCA(n_components=dimensions)

    def run(self, distance_matrix: DistanceMatrix) -> Chromosome:
        result_points = self.calculator.fit_transform(distance_matrix.distance_matrix_nparray)
        result_chromosome = Chromosome.from_points(result_points)
        return result_chromosome
