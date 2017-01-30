from space.DistanceMatrix import DistanceMatrix
from graph.ShortestDistancesFillerBase import ShortestDistancesFillerBase

import numpy as np
import igraph


class ShortestDistancesFillerIGraph(ShortestDistancesFillerBase):

    def fill(self, distance_matrix_with_gaps: DistanceMatrix) -> DistanceMatrix:

        #g = Graph.Adjacency((distance_matrix_with_gaps.distance_matrix_nparray != math.inf).tolist())
        g = igraph.Graph.Weighted_Adjacency(distance_matrix_with_gaps.distance_matrix_nparray.tolist(),
                                            mode=igraph.ADJ_UNDIRECTED)
        # g.vs["label"] = g.vs["name"] = range(0, 10)
        # visual_style = {}
        # visual_style["vertex_label"] = g.vs["name"]
        # visual_style["edge_width"] = g.es["weight"]
        # igraph.plot(g, **visual_style)

        distance_matrix_with_gaps_filled_list = g.shortest_paths_dijkstra(weights='weight')

        distance_matrix_with_gaps_filled = np.array(distance_matrix_with_gaps_filled_list)

        return DistanceMatrix(distance_matrix_with_gaps_filled)

