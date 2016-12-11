import random

from fitness.FitnessCalculator import FitnessCalculator
from ga.crossover.CrossovererBase import CrossoverrerBase
from ga.mutator.MutatorBase import MutatorBase
from ga.Population import Population

class Breeder:

    def __init__(self, initial_population: Population,
                 fitness_calculator: FitnessCalculator,
                 crossoverer: CrossoverrerBase,
                 mutator: MutatorBase):
        self.current_population = initial_population
        self.fitness_calculator = fitness_calculator
        self.crossoverer = crossoverer
        self.mutator = mutator
        self.population_size = initial_population.size
        self.generation = 0

    def breed(self):

        # calculate fitness
        scores = []
        for org in self.current_population.organisms:
            org.fitness_score = self.fitness_calculator.calculate(org.genome)
            scores.append(org.fitness_score)

        # create probability roulette wheel
        rw_scores = self.construct_roulette_wheel_score_array(scores)
        rw_total = sum(rw_scores)

        # fill offspring pool by crossing over two parents (pick up frim roulette wheel)
        new_generation = []
        while len(new_generation) != self.population_size:
            parent1_id = self.roulette_wheel_selector(rw_scores, rw_total)
            parent2_id = self.roulette_wheel_selector(rw_scores, rw_total)
            if parent1_id == parent2_id:
                continue
            parent1 = self.current_population.organisms[parent1_id]
            parent2 = self.current_population.organisms[parent2_id]
            new_organism = self.crossoverer.crossover(parent1, parent2)
            new_generation.append(new_organism)

        # TODO: introduce mutations

        best_score = self.current_population.get_best_fitness()
        worst_score = self.current_population.get_worst_fitness()
        avg_score = self.current_population.get_average_fitness()

        self.current_population = Population(new_generation)
        self.generation += 1

        return [self.generation, best_score, worst_score, avg_score]

    def construct_roulette_wheel_score_array(self, scores):
        s_min = min(scores)
        norm_scores = [x - s_min for x in scores]
        s_norm_max = max(norm_scores)
        inv_norm_scores = [s_norm_max - x for x in norm_scores]
        s_inv_norm_min = min([x for x in inv_norm_scores if x != 0]) # TODO: COULD BO EMPTY
        inv_norm_scores_inc = [x + s_inv_norm_min for x in inv_norm_scores]
        return inv_norm_scores_inc

    def roulette_wheel_selector(self, scores, total):
        r = random.uniform(0, total)
        current = 0
        for i, s in enumerate(scores):
            current += s
            if current > r:
                return i



