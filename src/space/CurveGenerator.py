import numpy as np
import math


class CurveGenerator:
    """Generates series of points in shape of curve"""

    def __init__(self, radius: float) -> object:
        """
        :param radius: next point chosen approximately within this radius
        """
        self.radius = radius

    def generate(self, points_amount: int) -> np.array:

        seed = np.random.RandomState()
        start_point = seed.randint(0, 100, 3).astype(np.float)
        start_point = start_point.reshape((1, 3))

        points = np.zeros((points_amount, 3))
        points[0] = start_point

        for i in range(1, points_amount):
            r = seed.normal(self.radius, self.radius / 4)
            u = seed.uniform()
            v = seed.uniform()
            theta = u * math.pi * 2
            phi = 1 / math.cos(2 * v - 1)
            x = r * math.sin(theta) * math.cos(phi) + points[i - 1][0]
            y = r * math.sin(theta) * math.sin(phi) + points[i - 1][1]
            z = r * math.cos(theta) + points[i - 1][2]
            points[i] = [x, y, z]

        return points


