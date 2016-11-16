from sklearn.metrics import euclidean_distances
from timeit import default_timer as timer
import csv

from mds.MDSTorgerson import MDSTorgerson
from space.CurveGenerator import CurveGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData
from graph import ShortestDistancesFiller


def run(mds_runner, distances_with_sd_gaps):


    mds_result = mds_runner.run(distances_with_sd_gaps)

    distances_after_mds_torgerson = euclidean_distances(mds_torgerson_result)

    # compare results (original distances - after MDS distances)
    # draw graph


mds_runner = MDSTorgerson(dimensions=3)
curve_generator = CurveGenerator(radius=10)
shortest_distances_filler = ShortestDistancesFiller()
gaps_generator = OrderedPercentGapsGenerator()

points_amount = 200

points = curve_generator.generate(points_amount)

hic_data = HiCData(points, gaps_generator, percent_threshold=0.05)

# calculate SD for gaps
distances_with_sd_gaps = shortest_distances_filler.fill(hic_data.get_distance_matrix_with_gaps())

# create initial population

# cycle of GA runs
    # MDS
    # Distance matrix
    # Fitness scoring
    # Selection
    # Crossovers
    # mutations
    # Return new population


print('Running for {0} points...'.format(points_amount))
start = timer()
run(mds_runner, distances_with_sd_gaps)
end = timer()
execution_time = end - start
print('Finished in {0} for {1} points.'.format(execution_time, points_amount))
