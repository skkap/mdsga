import csv
import os
import time

import math

from fitness.FitnessCalculator import FitnessCalculator
from fitness.RMSEScoreCalculator import RMSEScoreCalculator
from graph.ShortestDistancesFiller import ShortestDistancesFiller
from helpers import files_helper
from mds.MDSMyTorgerson import MDSMyTorgerson
from space.HiCData import HiCData

from ga.InitialPopulationGenerator import InitialPopulationGenerator
from ga.Organism import Organism
from ga.Breeder import Breeder
from ga.crossover.SinglePointCrossoverer import SinglePointCrossoverer
from ga.mutator.RandomPointMutator import RandomPointMutator


population_size = 100
generations = 10
introduce_mutations = False # TODO: Implement

my_torgerson_mds_runner = MDSMyTorgerson()
rmse_score_calculator = RMSEScoreCalculator()
shortest_distances_filler = ShortestDistancesFiller()
initial_population_generator = InitialPopulationGenerator()

# result directory
exp_name = 'ga_{0}ps_{1}g'.format(population_size, generations)
result_dir = '../result/{0}_{1}/'.format(time.strftime("%Y-%m-%d-%H-%M"), exp_name)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# load sample

hic_data = HiCData.from_files('../samples/100_0.9_10_9f33b232970024055214133c551a84f2/')
distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()

# fill in shortest distances
distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)


not_gaps_values = distance_matrix_with_gaps.get_flatten_upper_triangular_matrix_by_coordinates(hic_data.not_gaps)
fitness_calculator = FitnessCalculator(
    score_calculator=rmse_score_calculator,
    mds=my_torgerson_mds_runner,
    not_gaps_values=not_gaps_values,
    not_gaps_coordinates=hic_data.not_gaps,
    size=hic_data.size)

# create initial population
original_organism_genome = distance_matrix_sd.get_flatten_upper_triangular_matrix_except_coordinates(hic_data.not_gaps)
original_organism = Organism(original_organism_genome)
initial_population = initial_population_generator.generate(original_organism, population_size)

adam_score = fitness_calculator.calculate(original_organism_genome)
print('ADAM\'s organism score: {0}'.format(adam_score))

futm_original = hic_data.chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
adam_distance_matrix = fitness_calculator.compose_distance_matrix(original_organism_genome)
adam_chromosome_after_mds = my_torgerson_mds_runner.run(adam_distance_matrix)
adam_futm = adam_chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
adam_full_score = rmse_score_calculator.calculate(adam_futm, futm_original)
print('ADAM\'s full matrix score: {0}'.format(adam_full_score))


# Check if all INITIAL POPULATION values are less then Adam's ones
c = 0
for o in initial_population.organisms:
    for i, v in enumerate(o.genome):
        if v > original_organism.genome[i]:
            c += 1
            print('!')

c = 0
futm_sd = distance_matrix_sd.get_flatten_upper_triangular_matrix()
for o in initial_population.organisms:
    o_dm = fitness_calculator.compose_distance_matrix(o.genome)
    futm_o = o_dm.get_flatten_upper_triangular_matrix()
    for i, v in enumerate(futm_o):
        if v > futm_sd[i] + 0.000001:
            c += 1
            print('!')


crossoverer = SinglePointCrossoverer()
mutator = RandomPointMutator(frequency_of_mutations=0.001, lower_bound=0, upper_bound=100)
breeder = Breeder(initial_population,
                  fitness_calculator=fitness_calculator,
                  crossoverer=crossoverer,
                  mutator=mutator)


gen_info =[]
for c in range(generations):
    info = breeder.breed()
    print('{0} gen. Best: {1}. Worst: {2}. Avg.: {3}'.format(info[0], info[1], info[2], info[3]))
    gen_info.append(info)

    # c = 0
    # for o in breeder.current_population.organisms:
    #     o_dm = fitness_calculator.compose_distance_matrix(o.genome)
    #     futm_o = o_dm.get_flatten_upper_triangular_matrix()
    #     for i, v in enumerate(futm_o):
    #         if v > futm_sd[i] + 0.000001:
    #             c += 1
    #             print('!')


ga_result_path = os.path.join(result_dir, 'ga_result.csv')
with open(ga_result_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['gen', 'best', 'worst', 'avg'])
    for info in gen_info:
        writer.writerow(info)


# check whole structure
futm_original = hic_data.chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
#find best organism score
best_organism = breeder.current_population.get_best_organism()
best_organism_dm = fitness_calculator.compose_distance_matrix(best_organism.genome)
futm_best_organism_before_mds = best_organism_dm.get_flatten_upper_triangular_matrix()
best_organism_after_mds = my_torgerson_mds_runner.run(best_organism_dm)
futm_best_organism_after_mds = best_organism_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
best_organism_full_score = rmse_score_calculator.calculate(futm_best_organism_after_mds, futm_original)
print('Best organism FULL score: {0}'.format(best_organism_full_score))

futm_adam_before_mds = distance_matrix_sd.get_flatten_upper_triangular_matrix()
adam_chromosome_after_mds = my_torgerson_mds_runner.run(distance_matrix_sd)
futm_adam_after_mds = adam_chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
adam_full_score = rmse_score_calculator.calculate(futm_adam_after_mds, futm_original)
print('ADAM organism FULL score: {0}'.format(adam_full_score))


# save results
adam_before_mds_scatter_path = os.path.join(result_dir, 'adam_before_mds.png')
files_helper.save_scatter_plot('Adam before mds', adam_before_mds_scatter_path, futm_original, futm_adam_before_mds)

adam_scatter_path = os.path.join(result_dir, 'adam.png')
files_helper.save_scatter_plot('Adam', adam_scatter_path, futm_original, futm_adam_after_mds)

adam_hist_path = os.path.join(result_dir, 'adam_hist.png')
adam_hist_name = 'ADAM error hist. RMSE: {0:.3f}'.format(adam_full_score)
files_helper.save_rmse_hist(adam_hist_name, adam_hist_path, futm_original, futm_adam_after_mds)


best_before_mds_scatter_path = os.path.join(result_dir, 'best_before_mds.png')
files_helper.save_scatter_plot('Best before mds', best_before_mds_scatter_path, futm_original, futm_best_organism_before_mds)

best_scatter_path = os.path.join(result_dir, 'best.png')
files_helper.save_scatter_plot('Best', best_scatter_path, futm_original, futm_best_organism_after_mds)

best_hist_path = os.path.join(result_dir, 'best_hist.png')
best_hist_name = 'BEST error hist. RMSE: {0:.3f}'.format(best_organism_full_score)
files_helper.save_rmse_hist(best_hist_name, best_hist_path, futm_original, futm_best_organism_after_mds)


# Check if all Best's values are less then Adam's ones
c = 0
for i, v in enumerate(futm_adam_before_mds):
    if v + 0.000001 < futm_best_organism_before_mds[i]:
        c += 1
        print('{0} - {1}'.format(v, futm_best_organism_before_mds[i]))
print('Found {0} values where Bests values are less then Adams ones!'.format(c))


# Histogram



