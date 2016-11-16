from timeit import default_timer as timer
import csv

from mds.MDSTorgerson import MDSTorgerson
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator


def run(mds_runner, chromosome):
    chromosome_after_mds = mds_runner.run(chromosome.distance_matrix)
    return chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()

current_mds_runner = MDSTorgerson(dimensions=3)
chromosome_generator = ChromosomeGenerator(radius=10)
gaps_generator = OrderedPercentGapsGenerator()

points_amount = 500
chromosome = chromosome_generator.generate(points_amount)
futm_original = chromosome.distance_matrix.get_flatten_upper_triangular_matrix()

print('Running for {0} points...'.format(points_amount))
start = timer()
futm_after_mds = run(current_mds_runner, chromosome)
end = timer()
execution_time = end - start
print('Finished in {0} for {1} points.'.format(execution_time, points_amount))

# compare results (original distances - after MDS distances)
# draw graph
