from ga.crossover.MiddlePointCrossoverer import MiddlePointCrossoverer
from ga.crossover.SinglePointCrossoverer import SinglePointCrossoverer
from ga.crossover.ThreePointCrossoverer import ThreePointCrossoverer
from ga.crossover.TwoPointCrossoverer import TwoPointCrossoverer
from ga.crossover.UniformCrossoverer import UniformPointCrossoverer


def get_crossoverer_by_type(crossoverer_type: str):
    if crossoverer_type == '1p':
        return SinglePointCrossoverer()
    elif crossoverer_type == '2p':
        return TwoPointCrossoverer()
    elif crossoverer_type == '3p':
        return ThreePointCrossoverer()
    elif crossoverer_type == 'mp':
        return MiddlePointCrossoverer()
    elif crossoverer_type == 'u':
        return UniformPointCrossoverer()
    else:
        raise RuntimeError('This type of crossover is not implemented: {0}'.format(crossoverer_type))