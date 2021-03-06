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

def run(mds_runner, distance_matrix):

    print('Running for {0} points...'.format(distance_matrix.size))
    print('Using {0}'.format(mds_runner.__str__()))
    start = timer()
    chromosome_after_mds = mds_runner.run(distance_matrix)
    futm_after_mds = chromosome_after_mds.distance_matrix.get_futm()
    end = timer()
    execution_time = end - start
    print('Finished in {0} for {1} points.'.format(execution_time, chromosome.size))

    # compare results (original distances - after MDS distances)
    futm_original = chromosome.distance_matrix.get_futm()
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

points_amount = 100
chromosome = chromosome_generator.generate(points_amount)
hic_data = HiCData(chromosome, gaps_generator, percent_threshold=0)

distance_matrix = hic_data.get_distance_matrix_with_gaps()

run(smacof_mds_runner, distance_matrix)
run(my_torgerson_mds_runner, distance_matrix)
