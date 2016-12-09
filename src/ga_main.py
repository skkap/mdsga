import csv
import time

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
from ga.Mutator import MutatorBase


population_size = 100
generations = 10
introduce_mutations = False

my_torgerson_mds_runner = MDSMyTorgerson()
rmse_score_calculator = RMSEScoreCalculator()

shortest_distances_filler = ShortestDistancesFiller()

initial_population_generator = InitialPopulationGenerator()

# TODO: load sample

hic_data = HiCData.from_files('../samples/100_0.9_10_1690c8cacc46fc948a55a35b18792310/')
distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()
distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)


# TODO: calculate SD

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

crossoverer = SinglePointCrossoverer()
mutator = MutatorBase()
breeder = Breeder(initial_population,
                  fitness_calculator=fitness_calculator,
                  crossoverer=crossoverer,
                  mutator=mutator)


gen_info =[]
for c in range(generations):
    info = breeder.breed()
    print('{0} gen. Best: {1}. Worst: {2}. Avg.: {3}'.format(c, info[0], info[1], info[2]))
    gen_info.append(info)

exp_file_name = '{0}_{1}g'.format(time.strftime("%Y_%m_%d_%H_%M"), generations)
with open(exp_file_name + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['best', 'worst', 'avg'])
    for info in gen_info:
        writer.writerow(info)


# check whole structure
futm_original = hic_data.chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
#find best organism score
best_organism = breeder.current_population.get_best_organism()
best_organism_dm = fitness_calculator.compose_distance_matrix(best_organism.genome)
best_organism_chromosome_after_mds = my_torgerson_mds_runner.run(best_organism_dm)
futm_best_organism_after_mds = best_organism_chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
best_organism_full_score = rmse_score_calculator.calculate(futm_best_organism_after_mds, futm_original)
print('Best organism FULL score: {0}'.format(best_organism_full_score))

adam_chromosome_after_mds = my_torgerson_mds_runner.run(distance_matrix_sd)
futm_adam_after_mds = adam_chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix()
adam_full_score = rmse_score_calculator.calculate(futm_adam_after_mds, futm_original)
print('ADAM organism FULL score: {0}'.format(adam_full_score))


files_helper.save_scatter_plot(exp_file_name + '_adam', './', futm_original, futm_adam_after_mds)
files_helper.save_scatter_plot(exp_file_name + '_best', './', futm_original, futm_best_organism_after_mds)


# cnt = 0
# for org in initial_population.organisms:
#     futm_original = chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
#     futm_sd = distance_matrix_sd.get_flatten_upper_triangular_matrix()
#     file_name = os.path.basename(__file__) + str(cnt)
#     files_helper.save_scatter_plot(file_name, './', original_organism.genome, org.genome)
#     cnt += 1



# futm_original = chromosome.distance_matrix.get_flatten_upper_triangular_matrix()
# futm_sd = distance_matrix_sd.get_flatten_upper_triangular_matrix()
# file_name = os.path.basename(__file__) + '_sd'
# files_helper.save_scatter_plot(file_name, './', futm_original, futm_sd)


