import os
import math
import numpy as np
from numpy import genfromtxt

from helpers import files_helper

chromosome_names = [str(x) for x in range(1, 23)] + ['X']

hic_path = '../hic'

hic_file_path = os.path.join(hic_path, 'GSM2109887_K562-A-bulk-200kb.csv')

step = 200000

hic_data = genfromtxt(hic_file_path, delimiter=',', dtype=('|S2', '|S2', int, int, int, int, int))

hic_data = np.delete(hic_data, 0, axis=0)

interchromasomal_count = 0

chromosomes = {}

# chromosome dictionary init
for chromosome_name in chromosome_names:
    chromosomes[chromosome_name] = {
        'min': math.inf,
        'max': 0,
        'data': None
    }

# find size of each matrix
for e in hic_data:
    c1 = e[0].decode("utf-8")
    c2 = e[1].decode("utf-8")
    c1_st = e[2]
    c2_st = e[4]

    if c1 != c2:  # interchromasomal contacts
        interchromasomal_count += 1
        continue

    c1_pos = int(c1_st / step)
    c2_pos = int(c2_st / step)

    if chromosomes[c1]['min'] > c1_pos:
        chromosomes[c1]['min'] = c1_pos
    if chromosomes[c1]['max'] < c1_pos:
        chromosomes[c1]['max'] = c1_pos
    if chromosomes[c1]['min'] > c2_pos:
        chromosomes[c1]['min'] = c2_pos
    if chromosomes[c1]['max'] < c2_pos:
        chromosomes[c1]['max'] = c2_pos

for chromosome_name in chromosome_names:
    size = int(chromosomes[chromosome_name]['max'] - chromosomes[chromosome_name]['min'])
    chromosomes[chromosome_name]['data'] = np.full((size + 1, size + 1), -100)

    # for n in range(size):
    #     chromosomes[chromosome_name]['data'][n][n] = 0


for e in hic_data:
    c1 = e[0].decode("utf-8")
    c2 = e[1].decode("utf-8")
    c1_st = e[2]
    c2_st = e[4]
    count = e[6]

    if c1 != c2:  # interchromasomal contacts
        continue

    c1_pos = int(c1_st / step) - chromosomes[c1]['min']
    c2_pos = int(c2_st / step) - chromosomes[c1]['min']

    if c1_pos == c2_pos:
        continue

    chromosomes[c1]['data'][c1_pos][c2_pos] = chromosomes[c1]['data'][c2_pos][c1_pos] = count


# dm_path = os.path.join(directory, 'dm.npy')
# np.save(dm_path, chromosome.distance_matrix.distance_matrix_nparray)

hic_size = hic_data.size

print('All contacts: {}'.format(hic_data.size))
print('Interchromosomal contacts: {}({:2.2f}%)'.format(interchromasomal_count,
                                                       (interchromasomal_count * 100) / hic_size))

for chromosome_name in chromosome_names:
    chromosomes[chromosome_name]['gaps'] = 0
    for x in chromosomes[chromosome_name]['data']:
        for y in x:
            if y == -100:
                chromosomes[chromosome_name]['gaps'] += 1
    gaps = chromosomes[chromosome_name]['gaps']
    size = chromosomes[chromosome_name]['data'].shape[0]
    print('Chromosome `{}` gaps: {} ({:2.2f}%), points: {}'.format(chromosome_name,
                                                                   gaps,
                                                                   (gaps * 100) / (size * size),
                                                                   size))

for chromosome_name in chromosome_names:

    name = '200k_' + chromosome_name
    adj_path = os.path.join(hic_path, name + '.png')
    files_helper.save_adjastency_matrix(name, adj_path, chromosomes[chromosome_name]['data'])
