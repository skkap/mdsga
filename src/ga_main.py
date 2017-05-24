import csv
import os
import time
from datetime import timedelta, datetime

from exceptions.NoDiversityException import NoDiversityException
from fitness.FitnessCalculator import FitnessCalculator
from fitness.RMSEScoreCalculator import RMSEScoreCalculator
from ga.Breeder import Breeder
from ga.InitialPopulationGenerator import InitialPopulationGenerator
from ga.Organism import Organism
from ga.crossover.crossoverer_resolver import get_crossoverer_by_type
from ga.mutator.RandomPointMutator import RandomPointMutator
from graph.ShortestDistancesFillerIGraph import ShortestDistancesFillerIGraph
from helpers import files_helper
from mds.MDSMyTorgerson import MDSMyTorgerson
from sample.Sample import Sample
from util.command_line import get_ga_command_line_params

save_images = 0

params = get_ga_command_line_params()

my_torgerson_mds_runner = MDSMyTorgerson()
rmse_score_calculator = RMSEScoreCalculator()
shortest_distances_filler = ShortestDistancesFillerIGraph()
initial_population_generator = InitialPopulationGenerator()

crossoverer = get_crossoverer_by_type(params.crossoverer_type)

print('Starting MDSGA... ')
print('Generations: {0}; population size: {1}; mutation rate: {2}; check generations: {3}; crossoverer: {4}'
      .format(params.generations, params.population_size, params.mutation_rate,
              params.check_generations, params.crossoverer_type))

print('Loading sample... ', end='')
start = time.time()
sample = Sample(params.sample_path)
hic_data = sample.hic_data
distance_matrix_with_gaps = hic_data.get_distance_matrix_with_gaps()
end = time.time()
elapsed = end - start
print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))
print('📖  Sample "{0}" [{1} points, {2} known dist.] is loaded successfully.'
      .format(hic_data.name, hic_data.size, len(hic_data.not_gaps)))

not_gaps_values = distance_matrix_with_gaps.get_futm_by_coordinates(hic_data.not_gaps)
fitness_calculator = FitnessCalculator(
    score_calculator=rmse_score_calculator,
    mds=my_torgerson_mds_runner,
    not_gaps_values=not_gaps_values,
    not_gaps_coordinates=hic_data.not_gaps,
    size=hic_data.size)

if sample.initial_organism is not None and sample.initial_population is not None:
    print('Initial population loaded: {0} organisms'.format(sample.initial_population.size))
    initial_organism = sample.initial_organism
    initial_population = sample.initial_population
else:
    print('Running shortest distances algorithm... ', end='')
    start = time.time()
    distance_matrix_sd = shortest_distances_filler.fill(distance_matrix_with_gaps)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

    print('Generating initial organism (ADAM)... ', end='')
    start = time.time()
    initial_organism_genome = distance_matrix_sd.get_futm_except_ordered_coordinates(hic_data.not_gaps)
    initial_organism = Organism(initial_organism_genome)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

    print('Generating initial population... ', end='')
    start = time.time()
    initial_population = initial_population_generator.generate(initial_organism, params.population_size)
    end = time.time()
    elapsed = end - start
    print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))

print('Calculating ADAM\'s error... ', end='')
start = time.time()
adam_score = fitness_calculator.calculate(initial_organism.genome)
end = time.time()
elapsed = end - start
print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))
print('❗ ADAM\'s error: {0:.3f}'.format(adam_score))

print('Calculating ADAM\'s FULL error... ', end='')
start = time.time()
futm_original = hic_data.chromosome.distance_matrix.get_futm()
adam_distance_matrix = fitness_calculator.compose_distance_matrix(initial_organism.genome)
futm_adam_before_mds = adam_distance_matrix.get_futm()
adam_chromosome_after_mds = my_torgerson_mds_runner.run(adam_distance_matrix)
adam_after_mds_futm = adam_chromosome_after_mds.distance_matrix.get_futm()
adam_full_error = rmse_score_calculator.calculate(adam_after_mds_futm, futm_original)
end = time.time()
elapsed = end - start
print('Finished in {0} sec.'.format(timedelta(seconds=elapsed)))
print('❗️ ADAM\'s FULL error: {0:.3f}'.format(adam_full_error))

mutator = RandomPointMutator(frequency_of_mutations=params.mutation_rate, initial_organism=initial_organism,
                             divider=3)
breeder = Breeder(initial_population,
                  fitness_calculator=fitness_calculator,
                  crossoverer=crossoverer,
                  mutator=mutator)


gen_info = []
for c in range(1, params.generations + 1):
    start = time.time()

    try:
        info = breeder.breed()
    except NoDiversityException as e:
        print('No diversity in the population. Terminating...')
        break

    end = time.time()
    elapsed = end - start
    print('▷  {0}/{1}  gen. Time: {2}. B: {3:.3f}. W: {4:.3f}. A: {5:.3f}'
          .format(c, params.generations, timedelta(seconds=elapsed), info[1], info[2], info[3]))
    info.append(elapsed)
    gen_info.append(info)

    if c == 1:
        print('One generation takes about {0} sec.'.format(timedelta(seconds=elapsed)))
        time_until_end = timedelta(seconds=elapsed * (params.generations - 1))
        print('For {0} generations it will take about {1} sec.'.format(params.generations, time_until_end))
        finish_time = datetime.now() + time_until_end
        print('⏰ Will finish around {0}!'.format(finish_time))

    if c in params.check_generations:
        # find best organism score
        best_organism = breeder.current_population.get_best_organism()
        best_organism_dm = fitness_calculator.compose_distance_matrix(best_organism.genome)
        # futm_best_organism_before_mds = best_organism_dm.get_futm()
        best_organism_after_mds = my_torgerson_mds_runner.run(best_organism_dm)
        futm_best_organism_after_mds = best_organism_after_mds.distance_matrix.get_futm()
        best_organism_full_score = rmse_score_calculator.calculate(futm_best_organism_after_mds, futm_original)

        print('❗️ BEST FULL: {0:.3f}'.format(best_organism_full_score))


# result directory
exp_name = 'ga_{0}_{1}ps_{2}g_{3}m_{4}'.format(hic_data.name, initial_population.size,
                                               params.generations, params.mutation_rate, params.crossoverer_type)
result_dir = '../result/{0}_{1}/'.format(time.strftime("%Y-%m-%d-%H-%M"), exp_name)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


ga_result_path = os.path.join(result_dir, 'ga_result.csv')
with open(ga_result_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['gen', 'best', 'worst', 'avg'])
    for info in gen_info:
        writer.writerow(info)


# find best organism score
best_organism = breeder.current_population.get_best_organism()
best_organism_dm = fitness_calculator.compose_distance_matrix(best_organism.genome)
futm_best_organism_before_mds = best_organism_dm.get_futm()
best_organism_after_mds = my_torgerson_mds_runner.run(best_organism_dm)
futm_best_organism_after_mds = best_organism_after_mds.distance_matrix.get_futm()
best_organism_full_score = rmse_score_calculator.calculate(futm_best_organism_after_mds, futm_original)
print('Best organism FULL score: {0:.3f}'.format(best_organism_full_score))
print('ADAM organism FULL score: {0:.3f}'.format(adam_full_error))

try:
    # save results
    adam_before_mds_scatter_path = os.path.join(result_dir, 'adam_before_mds.png')
    files_helper.save_scatter_plot('Adam before mds', adam_before_mds_scatter_path, futm_original, futm_adam_before_mds)

    adam_scatter_path = os.path.join(result_dir, 'adam.png')
    files_helper.save_scatter_plot('Adam', adam_scatter_path, futm_original, adam_after_mds_futm)

    adam_hist_path = os.path.join(result_dir, 'adam_hist.png')
    adam_hist_name = 'ADAM error hist. RMSE: {0:.3f}'.format(adam_full_error)
    files_helper.save_rmse_hist(adam_hist_name, adam_hist_path, futm_original, adam_after_mds_futm)

    best_before_mds_scatter_path = os.path.join(result_dir, 'best_before_mds.png')
    files_helper.save_scatter_plot('Best before mds', best_before_mds_scatter_path, futm_original,
                                   futm_best_organism_before_mds)

    best_scatter_path = os.path.join(result_dir, 'best.png')
    files_helper.save_scatter_plot('Best', best_scatter_path, futm_original, futm_best_organism_after_mds)

    best_hist_path = os.path.join(result_dir, 'best_hist.png')
    best_hist_name = 'BEST error hist. RMSE: {0:.3f}'.format(best_organism_full_score)
    files_helper.save_rmse_hist(best_hist_name, best_hist_path, futm_original, futm_best_organism_after_mds)
except Exception as e:
    print('Cannot save images: {0}'.format(e))
