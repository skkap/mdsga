from mds.MDSBase import MDSBase
from sklearn import decomposition
import numpy as np


class MDSTorgerson(MDSBase):
    """MDS implementation in sklearn.decomposition.PCA, determinated Principal component analysis (PCA),
     traditional Torgerson algorithm"""

    def __init__(self, dimensions=3):
        self.calculator = decomposition.PCA(n_components=dimensions)

    def run(self, distance_matrix: np.array) -> np.array:
        result = self.calculator.fit_transform(distance_matrix)
        return result
