import argparse


class GAParams:
    sample_path = None
    population_size = None
    generations = None
    mutation_rate = None
    introduce_mutations = None
    check_generations = None
    crossoverer_type = None


class SampleGeneratorParams:
    points_amount = None
    percent_of_gaps = None
    radius = None
    save_initial_population = None
    population_size = None


def get_ga_command_line_params():
    population_size_default = 100
    generations_default = 10
    mutation_rate_default = 0.001
    check_generations_default = []
    crossoverer_type_default = '1p'

    argparser = argparse.ArgumentParser(description='Generates sample Hi-C experimental data')
    argparser.add_argument('path', metavar='PATH', type=str,
                           help='path to sample folder')
    argparser.add_argument('-p', '--population', dest='population_size', type=int,
                           default=population_size_default, help='size of population for GA')
    argparser.add_argument('-g', '--generations', dest='generations', type=int,
                           default=generations_default, help='number of generations for GA')
    argparser.add_argument('-m', '--mutation-rate', dest='mutation_rate', type=float,
                           default=mutation_rate_default, help='mutation rate (0..1')
    argparser.add_argument('--cg', dest='check_generations', nargs='*', type=int, default=check_generations_default,
                           help='generations on which FULL error is calculated')
    argparser.add_argument('-c', '--crossoverer', dest='crossoverer_type', default=crossoverer_type_default,
                           const=crossoverer_type_default, nargs='?', choices=['1p', '2p', '3p', 'mp', 'u'],
                           help='type of crossoverer')

    args = argparser.parse_args()

    ga_params = GAParams()
    ga_params.sample_path = args.path
    ga_params.population_size = args.population_size
    ga_params.generations = args.generations
    ga_params.mutation_rate = args.mutation_rate
    ga_params.introduce_mutations = (args.mutation_rate != 0)
    ga_params.check_generations = args.check_generations
    ga_params.crossoverer_type = args.crossoverer_type

    return ga_params


def get_sample_generator_params():
    radius_default = 10
    percent_of_gaps_default = 0.95
    points_amount_default = 100
    population_size_default = 100

    argparser = argparse.ArgumentParser(description='Generates sample Hi-C experimental data')
    argparser.add_argument('-r', '--radius', dest='radius', type=float,
                           default=radius_default, help='radius between each point (+/- radius divided by 4)')
    argparser.add_argument('-pog', '--percent-of-gaps', dest='percent_of_gaps', type=float,
                           default=percent_of_gaps_default, help='percent of gaps introduced to distance matrix (0..1)')
    argparser.add_argument('-p', '--points', dest='points_amount', type=int,
                           default=points_amount_default, help='amount of points in sample model')
    argparser.add_argument('-ip', '--save-ip', dest='save_initial_population', action='store_true')
    argparser.add_argument('--population', dest='population_size', type=int,
                           default=population_size_default, help='size of population for GA')
    args = argparser.parse_args()

    sample_generator_params = SampleGeneratorParams()
    sample_generator_params.points_amount = args.points_amount
    sample_generator_params.percent_of_gaps = args.percent_of_gaps
    sample_generator_params.radius = args.radius
    sample_generator_params.save_initial_population = args.save_initial_population
    sample_generator_params.population_size = args.population_size
    return sample_generator_params
