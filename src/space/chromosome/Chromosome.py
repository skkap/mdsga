from space.DistanceMatrix import DistanceMatrix


class Chromosome:

    def __init__(self, points):
        self.size = points.shape[0]
        self.points = points
        self.distance_matrix = DistanceMatrix(self.points)
