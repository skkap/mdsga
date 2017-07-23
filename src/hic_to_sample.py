import os
from operator import itemgetter

import numpy as np
from numpy import genfromtxt

from helpers import files_helper

chromosome_names = [str(x) for x in range(1, 23)] + ['X']

hic_path = '../hic'

hic_file_path = os.path.join(hic_path, 'GSM2109887_K562-A-bulk-200kb.csv')

step = 200000

gap_value = -1

hic_data = genfromtxt(hic_file_path, delimiter=',', dtype=('|S2', '|S2', int, int, int, int, int))

hic_data = np.delete(hic_data, 0, axis=0)

interchromasomal_count = 0

chromosomes = {}

# chromosome dictionary init
for chromosome_name in chromosome_names:
    chromosomes[chromosome_name] = {
        'max_original': 0,
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

    if chromosomes[c1]['max_original'] < c1_pos:
        chromosomes[c1]['max_original'] = c1_pos
    if chromosomes[c1]['max_original'] < c2_pos:
        chromosomes[c1]['max_original'] = c2_pos

for chromosome_name in chromosome_names:
    size = int(chromosomes[chromosome_name]['max_original']) + 1
    chromosomes[chromosome_name]['size'] = size
    chromosomes[chromosome_name]['data'] = np.full((size, size), gap_value)

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

    c1_pos = int(c1_st / step)
    c2_pos = int(c2_st / step)

    chromosomes[c1]['data'][c1_pos][c2_pos] = chromosomes[c1]['data'][c2_pos][c1_pos] = count


# remove empty lines
for chromosome_name in chromosome_names:
    empty_lines = []
    cur_chromosome = chromosomes[chromosome_name]
    size = cur_chromosome['size']
    for n in range(size):
        is_n_empty = True
        for x in range(size):
            if x == n:
                continue  # skip diagonal
            if cur_chromosome['data'][x][n] != gap_value:
                is_n_empty = False
                break
        if is_n_empty:
            empty_lines.append(n)

    chromosomes[chromosome_name]['empty_lines'] = empty_lines
    print('Chromosome `{}` empty lines: {} ({:2.2f}%), points: {}'.format(chromosome_name,
                                                                          len(empty_lines),
                                                                          (len(empty_lines) * 100) / size,
                                                                          size))
for chromosome_name in chromosome_names:
    empty_lines = chromosomes[chromosome_name]['empty_lines']
    size = chromosomes[chromosome_name]['size']
    new_size = size - len(empty_lines)
    chromosomes[chromosome_name]['filtered_size'] = new_size
    filtered_data = np.full((new_size, new_size), 0)
    x_shift = 0
    for x in range(size):
        if x in empty_lines:
            x_shift += 1
            continue
        y_shift = 0
        for y in range(size):
            if y in empty_lines:
                y_shift += 1
                continue
            filtered_data[x - x_shift][y - y_shift] = chromosomes[chromosome_name]['data'][x][y]

    chromosomes[chromosome_name]['filtered_data'] = filtered_data


# invert distances
for chromosome_name in chromosome_names:
    size = chromosomes[chromosome_name]['filtered_size']
    inverted_data = np.full((size, size), 0, dtype='f')
    not_gaps = []
    for x in range(size):
        for y in range(size):
            if x == y:
                inverted_data[x][y] = 0
                continue
            if chromosomes[chromosome_name]['filtered_data'][x][y] == gap_value:
                inverted_data[x][y] = gap_value
            else:
                inverted_data[x][y] = 1 / chromosomes[chromosome_name]['filtered_data'][x][y]
    chromosomes[chromosome_name]['inverted_data'] = inverted_data


# not_gaps
for chromosome_name in chromosome_names:
    size = chromosomes[chromosome_name]['filtered_size']
    not_gaps = []
    for x in range(0, size):
        for y in range(x + 1, size):
            if x == y:
                continue
            if chromosomes[chromosome_name]['filtered_data'][x][y] != gap_value:
                not_gaps.append([x, y])
    chromosomes[chromosome_name]['not_gaps'] = sorted(not_gaps, key=itemgetter(0, 1))


hic_size = hic_data.size

print('All contacts: {}'.format(hic_data.size))
print('Interchromosomal contacts: {}({:2.2f}%)'.format(interchromasomal_count,
                                                       (interchromasomal_count * 100) / hic_size))

for chromosome_name in chromosome_names:
    chromosomes[chromosome_name]['gaps_amount'] = 0
    for x in chromosomes[chromosome_name]['data']:
        for y in x:
            if y == gap_value:
                chromosomes[chromosome_name]['gaps_amount'] += 1

    gaps_amount = chromosomes[chromosome_name]['gaps_amount']
    size = chromosomes[chromosome_name]['data'].shape[0]
    print('Chromosome `{}` gaps: {} ({:2.2f}%), points: {}'.format(chromosome_name,
                                                                   gaps_amount,
                                                                   (gaps_amount * 100) / (size * size),
                                                                   size))

for chromosome_name in chromosome_names:

    name = '200k_' + chromosome_name
    directory = os.path.join(hic_path, name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    dm_path = os.path.join(directory, 'dm.npy')
    np.save(dm_path, chromosomes[chromosome_name]['inverted_data'])

    not_gaps_path = os.path.join(directory, 'not_gaps.npy')
    np.save(not_gaps_path, chromosomes[chromosome_name]['not_gaps'])

    adj_path = os.path.join(directory, 'original.png')
    files_helper.save_adjastency_matrix(name + '_original', adj_path, chromosomes[chromosome_name]['data'])

    adj_path = os.path.join(directory, 'filtered.png')
    files_helper.save_adjastency_matrix(name + '_filtered', adj_path, chromosomes[chromosome_name]['filtered_data'])

    adj_path = os.path.join(directory, 'inv.png')
    files_helper.save_adjastency_matrix(name + '_inv', adj_path, chromosomes[chromosome_name]['inverted_data'])
