import os
import csv
import math

import helpers.files_helper as files_helper

from fitness.FitnessCalculator import FitnessCalculator
from fitness.RMSEScoreCalculator import RMSEScoreCalculator
from graph.ShortestDistancesFiller import ShortestDistancesFiller
from mds.MDSMyTorgerson import MDSMyTorgerson
from space.HiCData import HiCData
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from ga.InitialPopulationGenerator import InitialPopulationGenerator
from ga.Organism import Organism
from ga.Breeder import Breeder
from ga.crossover.SinglePointCrossoverer import SinglePointCrossoverer
from ga.Mutator import Mutator

points_amount = 100
percent_of_gaps = 0.9
population_size = 10


my_torgerson_mds_runner = MDSMyTorgerson()
rmse_score_calculator = RMSEScoreCalculator()

chromosome_generator = ChromosomeGenerator(radius=10)
gaps_generator = OrderedPercentGapsGenerator()
shortest_distances_filler = ShortestDistancesFiller()

initial_population_generator = InitialPopulationGenerator()

chromosome = chromosome_generator.generate(points_amount)
hic_data = HiCData(chromosome, gaps_generator, percent_threshold=percent_of_gaps)
distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()
distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)

# TODO: check integrity
if math.inf in distance_matrix_sd.distance_matrix_nparray:
    raise ValueError('SD could not reconstruct all distances')

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
mutator = Mutator()
breeder = Breeder(initial_population,
                  fitness_calculator=fitness_calculator,
                  crossoverer=crossoverer,
                  mutator=mutator)

for c in range(100):
    breeder.breed()
    print(c)



# with open('initial_population.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(scores)
#
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



# cycle of GA runs
    # MDS
    # Distance matrix
    # Fitness scoring
    # Selection
    # Crossovers
    # mutations
    # Return new population

