from space.DistanceMatrix import DistanceMatrix


class Chromosome:

    def __init__(self, points):

        if points.ndim != 2:
            raise ValueError('"points" should have two dimensions.')
        if points.shape[0] < 3:
            raise ValueError('"points" should contain at least 3 points.')
        if points.shape[1] != 3:
            raise ValueError('"points" should be X*3 (x,y,z).')

        self.size = points.shape[0]
        self.points = points
        self.distance_matrix = DistanceMatrix.from_points(self.points)
