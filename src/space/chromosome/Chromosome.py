from space.DistanceMatrix import DistanceMatrix


class Chromosome:

    def __init__(self, points):
        self.points = points
        self.distance_matrix = DistanceMatrix(self.points)
