from timeit import default_timer as timer
import os

import helpers.files_helper as files_helper
from mds.MDSTorgerson import MDSTorgerson
from mds.MDSSmacof import MDSSmacof
from mds.MDSMyTorgerson import MDSMyTorgerson
from fitness.RMSEScoreCalculator import RMSEScoreCalculator
from fitness.PearsonScoreCalculator import PearsonScoreCalculator
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData
from graph.ShortestDistancesFiller import ShortestDistancesFiller


def run(mds_runner, distance_matrix):

    print('Running for {0} points...'.format(distance_matrix.size))
    print('Using {0}'.format(mds_runner.__str__()))
    start = timer()
    chromosome_after_mds = mds_runner.run(distance_matrix)
    futm_after_mds = chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
    end = timer()
    execution_time = end - start
    print('Finished in {0} for {1} points.'.format(execution_time, chromosome.size))

    # compare results (original distances - after MDS distances)
    futm_original = chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
    rmse_fitness = rmse_fitness_calculator.calculate(futm_original, futm_after_mds)
    print('{0}: {1}'.format(rmse_fitness_calculator.__str__(), rmse_fitness))
    pearson_fitness = pearson_fitness_calculator.calculate(futm_original, futm_after_mds)
    print('{0}: {1}'.format(pearson_fitness_calculator.__str__(), pearson_fitness))

    file_name = os.path.basename(__file__) + '_' + mds_runner.__str__()
    files_helper.save_scatter_plot(file_name, './', futm_original, futm_after_mds)
    return

smacof_mds_runner = MDSSmacof(dimensions=3)
my_torgerson_mds_runner = MDSMyTorgerson()

rmse_fitness_calculator = RMSEScoreCalculator()
pearson_fitness_calculator = PearsonScoreCalculator()
chromosome_generator = ChromosomeGenerator(radius=10)
gaps_generator = OrderedPercentGapsGenerator()
shortest_distances_filler = ShortestDistancesFiller()

points_amount = 100
chromosome = chromosome_generator.generate(points_amount)
hic_data = HiCData(chromosome, gaps_generator, percent_threshold=0.9)

distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()

distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)

futm_original = chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
futm_sd = distance_matrix_sd.get_flatten_upper_triangular_matrix()
file_name = os.path.basename(__file__) + '_sd'
files_helper.save_scatter_plot(file_name, './', futm_original, futm_sd)

run(smacof_mds_runner, distance_matrix_sd)
run(my_torgerson_mds_runner, distance_matrix_sd)
