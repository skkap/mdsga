from abc import ABCMeta, abstractmethod

from ga.Organism import Organism

class MutatorBase(metaclass=ABCMeta):

    @abstractmethod
    def introduce(self, organism: Organism):
        pass