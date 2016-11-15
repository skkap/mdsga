from sklearn.metrics import euclidean_distances
from timeit import default_timer as timer
import csv

from mds.MDSSmacof import MDSSmacof
from mds.MDSTorgerson import MDSTorgerson
from space.CurveGenerator import CurveGenerator
from graph import ShortestDistancesFiller


def run(shortest_distances_filler, mds_runner, distances):

    # calculate SD for gaps
    distances_with_sd_gaps = shortest_distances_filler.fill(distances, gaps)

    mds_result = mds_runner.run(distances)

    #distances_after_mds_torgerson = euclidean_distances(mds_torgerson_result)

    # compare results (original distances - after MDS distances)
    # draw graph


mds_runner = MDSTorgerson(dimensions=3)
curve_generator = CurveGenerator(radius=10)
shortest_distances_filler = ShortestDistancesFiller()

points_amount = 200

points = curve_generator.generate(points_amount)

distances = euclidean_distances(points)

# introduce gaps into distance matrix

print('Running for {0} points...'.format(points_amount))
start = timer()
run(shortest_distances_filler, mds_runner, distances)
end = timer()
execution_time = end - start
print('Finished in {0} for {1} points.'.format(execution_time, points_amount))
