import math
import os
import time
from datetime import timedelta

import numpy as np
import sys

import helpers.files_helper as files_helper
from ga.InitialPopulationGenerator import InitialPopulationGenerator
from ga.Organism import Organism
from graph.ShortestDistancesFillerIGraph import ShortestDistancesFillerIGraph
from space.HiCData import HiCData
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from util.command_line import get_sample_generator_params

sample_dir = '../samples/'

params = get_sample_generator_params()

print('Generating HiC Data...')
print('Amount of points: {0}'.format(params.points_amount))
print('Percent of gaps: {0}'.format(params.percent_of_gaps))
print('Radius: {0}'.format(params.radius))

chromosome_generator = ChromosomeGenerator(radius=params.radius)
gaps_generator = OrderedPercentGapsGenerator()
shortest_distances_filler = ShortestDistancesFillerIGraph()

tries = 0
while True:
    print('Try {0}'.format(tries))

    print('Generating chromosome...')
    start = time.time()
    chromosome = chromosome_generator.generate(params.points_amount)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

    print('Generating Hi-C data with gaps...')
    start = time.time()
    hic_data = HiCData.from_chromosome_with_gaps_generation(chromosome, gaps_generator,
                                                            percent_threshold=params.percent_of_gaps)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

    print('Constructing DM with gaps...')
    start = time.time()
    distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

    # check integrity
    print('Checking integrity...')
    start = time.time()
    distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))
    if math.inf not in distance_matrix_sd.distance_matrix_nparray:
        print('Successfully generated with {0} tries!'.format(tries))
        break
    print('SD could not reconstruct all distances.')
    tries += 1

hic_data_hash = hic_data.chromosome.get_hash()[:8]
sample_name = '{0}_{1}_{2}_{3}'.format(params.points_amount, params.percent_of_gaps, params.radius, hic_data_hash)
print('Saving "{0}"...'.format(sample_name))

directory = os.path.join(sample_dir, sample_name)
if not os.path.exists(directory):
    os.makedirs(directory)

points_path = os.path.join(directory, 'points.npy')
np.save(points_path, chromosome.points)

dm_path = os.path.join(directory, 'dm.npy')
np.save(dm_path, chromosome.distance_matrix.distance_matrix_nparray)

not_gaps_path = os.path.join(directory, 'not_gaps.npy')
np.save(not_gaps_path, hic_data.not_gaps)

curve_path = os.path.join(directory, 'curve.pdf')
files_helper.save_3d_plot(sample_name, curve_path, chromosome.points)

adj_path = os.path.join(directory, 'adj.png')
files_helper.save_adjastency_matrix(sample_name, adj_path, chromosome.distance_matrix.distance_matrix_nparray)

if not params.save_initial_population:
    print('Saved!')
    sys.exit()

initial_organism_genome = distance_matrix_sd.get_futm_except_ordered_coordinates(hic_data.not_gaps)
initial_organism = Organism(initial_organism_genome)
initial_population_generator = InitialPopulationGenerator()
initial_population = initial_population_generator.generate(initial_organism, params.population_size)

initial_organism_path = os.path.join(directory, 'initial_organism.npy')
initial_organism.save(initial_organism_path)

initial_population_path = os.path.join(directory, 'initial_population.npy')
initial_population.save(initial_population_path)
print('Saved!')