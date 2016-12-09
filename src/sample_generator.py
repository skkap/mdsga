import math
import os
import numpy as np

from space.chromosome.ChromosomeGenerator import ChromosomeGenerator
from space.gaps_genetrator.OrderedPercentGapsGenerator import OrderedPercentGapsGenerator
from space.HiCData import HiCData
from graph.ShortestDistancesFiller import ShortestDistancesFiller


sample_dir = '../samples/'

points_amount = 100
percent_of_gaps = 0.9
radius = 10

print('Generating HiC Data...')
print('Amount of points: {0}'.format(points_amount))
print('Percent of gaps: {0}'.format(percent_of_gaps))
print('Radius: {0}'.format(radius))

chromosome_generator = ChromosomeGenerator(radius=radius)
gaps_generator = OrderedPercentGapsGenerator()
shortest_distances_filler = ShortestDistancesFiller()

tries = 0
while True:
    print('Try {0}'.format(tries))
    chromosome = chromosome_generator.generate(points_amount)
    hic_data = HiCData.from_chromosome_with_gaps_generation(chromosome, gaps_generator, percent_threshold=percent_of_gaps)
    distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()

    # check integrity
    distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)
    if math.inf in distance_matrix_sd.distance_matrix_nparray:
        print('SD could not reconstruct all distances.')
        tries += 1
        continue

    hic_data_hash = hic_data.chromosome.get_hash()
    sample_name = '{0}_{1}_{2}_{3}'.format(points_amount, percent_of_gaps, radius, hic_data_hash)
    print('Successfully generated. Saving "{0}"'.format(sample_name))

    # save structure
    directory = os.path.join(sample_dir, sample_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    points_path = os.path.join(directory, 'points.txt')
    np.savetxt(points_path, chromosome.points)

    dm_path = os.path.join(directory, 'dm.txt')
    np.savetxt(dm_path, chromosome.distance_matrix.distance_matrix_nparray)

    not_gaps_path = os.path.join(directory, 'not_gaps.txt')
    np.savetxt(not_gaps_path, hic_data.not_gaps, '%1.1d')

    break
