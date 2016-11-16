from timeit import default_timer as timer
import csv

import helpers.files_helper as files_helper
from mds.MDSTorgerson import MDSTorgerson
from mds.MDSSmacof import MDSSmacof
from mds.MDSMyTorgerson import MDSMyTorgerson
from fitness.RMSEFitnessCalculator import RMSEFitnessCalculator
from fitness.PearsonFitnessCalculator import PearsonFitnessCalculator
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator


def run(mds_runner, chromosome):

    print('Running for {0} points...'.format(chromosome.size))
    print('Using {0}'.format(mds_runner.__str__()))
    start = timer()
    chromosome_after_mds = mds_runner.run(chromosome.distance_matrix)
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

    files_helper.save_scatter_plot(mds_runner.__str__(), './', futm_original, futm_after_mds)
    return

smacof_mds_runner = MDSSmacof(dimensions=3)
torgerson_mds_runner = MDSTorgerson(dimensions=3)
my_torgerson_mds_runner = MDSMyTorgerson()

rmse_fitness_calculator = RMSEFitnessCalculator()
pearson_fitness_calculator = PearsonFitnessCalculator()
chromosome_generator = ChromosomeGenerator(radius=10)
gaps_generator = OrderedPercentGapsGenerator()

points_amount = 500
chromosome = chromosome_generator.generate(points_amount)

run(smacof_mds_runner, chromosome)
run(torgerson_mds_runner, chromosome)
run(my_torgerson_mds_runner, chromosome)

# draw graph
