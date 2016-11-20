from fitness.ScoreCalculatorBase import ScoreCalculatorBase

class Population:

    def __init__(self, fitness_calculator: ScoreCalculatorBase, organisms: list):
        self.organisms = organisms
        self.fitness_calculator = fitness_calculator

    def calculate_fitness(self):
        for organism in self.organisms:
            fitness = self.fitness_calculator.calculate()


