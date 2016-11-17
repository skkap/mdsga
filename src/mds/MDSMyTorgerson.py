from mds.MDSBase import MDSBase
from sklearn import decomposition
import numpy as np

from space.DistanceMatrix import DistanceMatrix
from space.chromosome.Chromosome import Chromosome


class MDSMyTorgerson(MDSBase):
    """MDS my implementation traditional Torgerson algorithm"""

    def __str__(self):
        return 'MDS MY Torgerson algorithm'

    def run(self, distance_matrix: DistanceMatrix) -> Chromosome:
        """
        Classical multidimensional scaling (MDS)
        http://www.nervouscomputer.com/hfs/cmdscale-in-python/

        Parameters
        ----------
        distance_matrix : distance matrix

        Returns
        -------
            Configuration matrix. Each column represents a dimension. Only the
            p dimensions corresponding to positive eigenvalues of B are returned.
            Note that each dimension is only determined up to an overall sign,
            corresponding to a reflection.
        """
        D = distance_matrix.distance_matrix_nparray

        # Number of points
        n = distance_matrix.size

        # Centering matrix
        H = np.eye(n) - np.ones((n, n)) / n

        # YY^T
        B = -H.dot(D ** 2).dot(H) / 2

        # Diagonalize
        evals, evecs = np.linalg.eigh(B)

        # Sort by eigenvalue in descending order
        idx = np.argsort(evals)[::-1]
        evals = evals[idx]
        evecs = evecs[:, idx]

        # Compute the coordinates using positive-eigenvalued components only
        w, = np.where(evals > 0)
        L = np.diag(np.sqrt(evals[w]))
        V = evecs[:, w]
        Y = V.dot(L)

        #return Y, evals
        result_points = np.delete(Y, np.s_[3:], 1)

        result_chromosome = Chromosome(result_points)
        return result_chromosome
