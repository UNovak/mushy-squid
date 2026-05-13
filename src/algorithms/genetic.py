import math
import random

from utils.ga_helpers import validate_seq
from utils.helpers import timer
from utils.models import Data, Solution


def generate_individual(data: Data) -> list[int]:
    """
    Returns one randomly generated solution.
    seq: [2,4,5,3,6]
    """
    unvisited = set(data.ids)  # get all customer node_ids
    seq: list[int] = []

    while unvisited:
        current_capacity = data.capacity
        possible_customer = list(unvisited)

        while possible_customer:
            id = random.choice(possible_customer)  # pick a random node
            current_capacity -= data.demands[id]  # update truck capacity
            seq.append(id)  # add id to path
            unvisited.remove(id)  # mark node as visited, remove it from set

            # update possible customers based on unvisited nodes and remaining truck capacity
            possible_customer = [id for id in unvisited if data.demands[id] <= current_capacity]

    return seq


def mutate(seq: list[int], rate) -> list[int]:
    """
    Takes a sequence and mutates it.
    Returns the new sequence [2,5,3,4,6]
    """
    if random.random() < rate:
        idx1, idx2 = random.sample(range(len(seq)), 2)
        seq[idx1], seq[idx2] = seq[idx2], seq[idx1]

    return seq


def tournament_selection(population, size=3) -> tuple[list[int], list[int]]:
    """returns the two cheapest sets of routes from each group"""

    def select_best():
        """returns the cheapest set of routes from the tournament_group"""
        max_size = min(size, len(population))
        group = random.sample(population, max_size)  # randomly select #size from population
        winner = min(group, key=lambda x: x[0])  # pick the lowest total cost
        return winner[1]  # return only the routes

    p1 = select_best()
    p2 = select_best()

    return p1, p2


def crossover(data: Data, p1: list[int], p2: list[int]) -> list[int]:
    """
    Takes two sets of routes.
    Returns a the child as a single sequence
    seq: [2,4,5,3,6]
    """
    # remove depot ids
    seq1: list[int] = [id for id in p1 if id != data.depot_id]
    seq2: list[int] = [id for id in p2 if id != data.depot_id]
    size = len(seq1)
    child = [0] * size  # empty array to fill using crossover

    # ordered crossover
    start, end = random.sample(range(size), 2)  # pick two random points
    child[start:end] = seq1[start:end]  # add selected part from p1

    # fill the child with remaining nodes from seq2
    seq2 = [x for x in seq2 if x not in child]
    idx = 0
    for i in range(size):
        # skip over the part populated from p1
        if child[i] == 0:
            child[i] = seq2[idx]
            idx += 1

    return child


def hybrid(
    data: Data,
    iterations: int = 100,
    tournament_size=3,
    mutation_rate: float = 0.3,
    population: list[tuple[float, list[int]]] | None = None,
) -> list[tuple[float, list[int]]]:
    """returns better half of the sorted population"""

    # scale the population size based on input
    population_size = math.floor((data.dimension / 2))

    # if initial population not provided
    # randomly generate the initial population
    if population is None:
        population = []
        iterations += 1
        for _ in range(population_size):
            individual = generate_individual(data)  # [2,3,4,5]
            cost, valid_individual = validate_seq(data, individual)  # (int, [1,2,3,1,4,5,1])
            population.append((cost, valid_individual))

        # sort the initial population
        population.sort(key=lambda x: x[0])

    # main loop
    for iteration in range(iterations - 1):
        next_gen = []

        # elitism
        elite_count = population_size // 10
        next_gen.extend(population[:elite_count])

        # create the next generation
        for _ in range(population_size - elite_count):
            p1, p2 = tournament_selection(population, tournament_size)
            child_seq = crossover(data, p1, p2)  # create a new solution
            child = mutate(child_seq, mutation_rate)  # mutate the solution
            child = validate_seq(data, child)  # fix the solution, calculate cost
            next_gen.append(child)

        # sort next_gen and update the population
        population = sorted(next_gen, key=lambda x: x[0])[:population_size]

    return population[: int(len(population) // 2)]


@timer
def run(data: Data, iterations: int = 100, tournament_size=3, mutation_rate: float = 0.3):
    population: list[tuple[int, list[int]]] = []
    tracker = []  # keep track of optimal solutions

    # scale the population size based on input
    population_size = math.floor((data.dimension / 2))

    # randomly generate the initial population
    for _ in range(population_size):
        individual = generate_individual(data)
        cost, valid_individual = validate_seq(data, individual)
        population.append((cost, valid_individual))

    # sort the initial population
    population.sort(key=lambda x: x[0])

    # store the best solution
    min_cost = population[0][0]

    # main loop
    for iteration in range(iterations - 1):
        next_gen = []

        # elitism
        elite_count = population_size // 10
        next_gen.extend(population[:elite_count])

        # create the next generation
        for _ in range(population_size - elite_count):
            p1, p2 = tournament_selection(population, tournament_size)
            child_seq = crossover(data, p1, p2)  # create a new solution
            child = mutate(child_seq, mutation_rate)  # mutate the solution
            child = validate_seq(data, child)  # fix the solution, calculate cost
            next_gen.append(child)

        # sort next_gen and update the population
        population = sorted(next_gen, key=lambda x: x[0])[:population_size]

        # check for new best solution
        if population[0][0] < min_cost:
            min_cost = population[0][0]  # update min_cost
            tracker.append((iteration, population[0]))  # store current best solution

    return Solution(population[0][0], population[0][1])
