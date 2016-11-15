import numpy as np


class ShortestDistancesFiller:

    def fill(self, distance_matrix_with_gaps: np.array) -> np.array:

        if distance_matrix_with_gaps.ndim != 2:
            raise ValueError('"distance_matrix_with_gaps" should have just two dimensions.')
        if distance_matrix_with_gaps.shape[0] != distance_matrix_with_gaps.shape[1]:
            raise ValueError('"distance_matrix_with_gaps" should be square matrix.')
        if distance_matrix_with_gaps.shape[0] < 3:
            raise ValueError('"distance_matrix_with_gaps" should be at least 3*3.')

        distance_matrix_with_gaps_filled = self.floyd_warshall(distance_matrix_with_gaps)
        return distance_matrix_with_gaps_filled

    def floyd_warshall(self, distance_matrix_with_gaps: np.array) -> np.array:
        """Solves all pair shortest path via Floyd Warshall Algrorithm"""

        n = distance_matrix_with_gaps.shape[0]

        """ dist[][] will be the output matrix that will finally
            have the shortest distances between every pair of vertices """
        """ initializing the solution matrix same as input graph matrix
        OR we can say that the initial values of shortest distances
        are based on shortest paths considerting no
        intermedidate vertices """
        dist = np.copy(distance_matrix_with_gaps)

        """ Add all vertices one by one to the set of intermediate
         vertices.
         ---> Before start of a iteration, we have shortest distances
         between all pairs of vertices such that the shortest
         distances consider only the vertices in set
        {0, 1, 2, .. k-1} as intermediate vertices.
          ----> After the end of a iteration, vertex no. k is
         added to the set of intermediate vertices and the
        set becomes {0, 1, 2, .. k}
        """
        for k in range(n):

            # pick all vertices as source one by one
            for i in range(n):

                # Pick all vertices as destination for the
                # above picked source
                # for j in range(n):
                for j in range(i):
                    # If vertex k is on the shortest path from
                    # i to j, then update the value of dist[i][j]
                    # dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                    dist[i][j] = dist[j][i] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist
