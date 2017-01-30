import argparse
import math
import os
import numpy as np
import time
from datetime import timedelta

import helpers.files_helper as files_helper
from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData
from graph.ShortestDistancesFillerIGraph import ShortestDistancesFillerIGraph


sample_dir = '../samples/'

radius_default = 10
percent_of_gaps_default = 0.95
points_amount_default = 100

argparser = argparse.ArgumentParser(description='Generates sample Hi-C experimental data')
argparser.add_argument('-r', '--radius', dest='radius', type=float,
                       default=radius_default, help='radius between each point (+/- radius divaded by 4)')
argparser.add_argument('-pog', '--percent-of-gaps', dest='percent_of_gaps', type=float,
                       default=percent_of_gaps_default, help='percent of gaps introduced to distance matrix (0..1)')
argparser.add_argument('-p', '--points', dest='points_amount', type=int,
                       default=points_amount_default, help='amount of points in sample model')
args = argparser.parse_args()


points_amount = args.points_amount
percent_of_gaps = args.percent_of_gaps
radius = args.radius

print('Generating HiC Data...')
print('Amount of points: {0}'.format(points_amount))
print('Percent of gaps: {0}'.format(percent_of_gaps))
print('Radius: {0}'.format(radius))

chromosome_generator = ChromosomeGenerator(radius=radius)
gaps_generator = OrderedPercentGapsGenerator()
shortest_distances_filler = ShortestDistancesFillerIGraph()

tries = 0
while True:
    print('Try {0}'.format(tries))

    print('Generating chromosome...')
    start = time.time()
    chromosome = chromosome_generator.generate(points_amount)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(str(timedelta(seconds=elapsed))))

    print('Generating Hi-C data with gaps...')
    start = time.time()
    hic_data = HiCData.from_chromosome_with_gaps_generation(chromosome, gaps_generator,
                                                            percent_threshold=1-percent_of_gaps)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(str(timedelta(seconds=elapsed))))

    print('Constructing DM with gaps...')
    start = time.time()
    distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(str(timedelta(seconds=elapsed))))

    # check integrity
    print('Checking integrity...')
    start = time.time()
    distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(str(timedelta(seconds=elapsed))))
    if math.inf not in distance_matrix_sd.distance_matrix_nparray:
        print('Successfully generated with {0} tries!'.format(tries))
        break
    print('SD could not reconstruct all distances.')
    tries += 1

hic_data_hash = hic_data.chromosome.get_hash()[:8]
sample_name = '{0}_{1}_{2}_{3}'.format(points_amount, percent_of_gaps, radius, hic_data_hash)
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

curve_path = os.path.join(directory, 'curve.png')
files_helper.save_3d_plot(sample_name, curve_path, chromosome.points)

print('Saved!')

