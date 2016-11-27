from abc import ABCMeta, abstractmethod

from ga.Organism import Organism


class CrossoverrerBase(metaclass=ABCMeta):

    @abstractmethod
    def crossover(self, organism1: Organism, organism2: Organism):
        pass