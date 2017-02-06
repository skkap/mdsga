import numpy as np
import math
from operator import itemgetter

from space.gaps_genetrator.GapsGeneratorBase import GapsGeneratorBase


class OrderedPercentGapsGenerator(GapsGeneratorBase):

    def get_not_gaps(self, distance_matrix: np.array, percent_threshold: float) -> list:
        """
        Returns list of positions in the distance matrix where there is no gap in order by rows
        :param distance_matrix: Distance matrix
        :param percent_threshold: What percentage of biggest distances will be turned into the gaps (0 ... 1)
        :return: Positions without gaps in order by rows
        """

        if percent_threshold < 0 or percent_threshold > 1:
            raise ValueError('"percent_threshold" should be between 0 and 1.')
        if distance_matrix.ndim != 2:
            raise ValueError('"distance_matrix" should have just two dimensions.')
        if distance_matrix.shape[0] != distance_matrix.shape[1]:
            raise ValueError('"distance_matrix" should be square matrix.')
        n = distance_matrix.shape[0]
        if n < 3:
            raise ValueError('"distance_matrix" should be at least 3*3.')

        not_gaps = []
        values = []
        for x in range(0, n):
            for y in range(x + 1, n):  # going just through the elements above diagonal
                values.append(
                    {
                        'distance': distance_matrix[x, y],
                        'position': [x, y]
                    })
        values = sorted(values, key=itemgetter('distance'))
        gaps_from_here_index = int(math.floor(len(values) * percent_threshold))

        for i in range(0, len(values) - gaps_from_here_index):
            not_gaps.append(values[i]['position'])

        sorted_not_gaps = sorted(not_gaps, key=itemgetter(0, 1))

        return sorted_not_gaps

