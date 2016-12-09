import hashlib

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

    def get_hash(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.points.tostring())
        # hash_md5.update(str(self.points))
        h = hash_md5.hexdigest()
        return h
