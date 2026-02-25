import math
import random

from utils.fix_routes import fix_routes
from utils.helpers import seq_to_routes
from utils.models import Data, Solution


def generate_individual(data: Data) -> list[list[int]]:
    """returns one randomly generated solution"""
    unvisited = set(data.ids)  # get all customer node_ids
    routes: list[list[int]] = []

    while unvisited:
        current_capacity = data.capacity
        possible_customer = list(unvisited)
        route: list[int] = []  # path of one vehicle

        while possible_customer:
            id = random.choice(possible_customer)  # pick a random node
            current_capacity -= data.demands[id]  # update truck capacity
            route.append(id)  # add id to path
            unvisited.remove(id)  # mark node as visited, remove it from set

            # update possible customers based on unvisited nodes and remaining truck capacity
            possible_customer = [id for id in unvisited if data.demands[id] <= current_capacity]

        # unvisited nodes, no possible customer
        routes.append(route)
    return routes


def mutate(data, seq: list[int], rate) -> list[list[int]]:
    """takes a sequence and mutates it, returns the new sequence"""
    if random.random() < rate:
        idx1, idx2 = random.sample(range(len(seq)), 2)
        seq[idx1], seq[idx2] = seq[idx2], seq[idx1]
    return seq_to_routes(data, seq)


def tournament_selection(population, size=3) -> tuple[list[list[int]], list[list[int]]]:
    """returns the two cheapest sets of routes from each grup"""

    def select_best():
        """returns the cheapest set of routes from the tournament_grup"""
        group = random.sample(population, size)  # randomly select #size from population
        winner = min(group, key=lambda x: x[0])  # pick the lowest total cost
        return winner[1]  # return only the routesa

    p1 = select_best()
    p2 = select_best()

    return p1, p2


def crossover(data: Data, p1: list[list[int]], p2: list[list[int]]) -> list[int]:
    """takes two sets of routes and returns a the child as a single sequence"""
    # flatten the routes
    seq1: list[int] = [id for route in p1 for id in route]
    seq2: list[int] = [id for route in p2 for id in route]
    size = len(seq1)
    child = [0] * size  # empty array to fill using crossover

    # ordered crossover
    start, end = random.sample(range(size), 2)  # pick two random points
    child[start:end] = seq1[start:end]  # add selected part from p1

    # fill the child with remaining nodes from seq2
    seq2 = [x for x in seq2 if x not in child]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = seq2[idx]
            idx += 1

    return child


def run(data: Data):
    generations: int = 100
    tournament_size = 3
    mutation_rate: float = 0.1
    population: list[tuple[int, list[list[int]]]] = []
    tracker = []  # keep track of optimal solutions

    # scale the population size based on input
    population_size = math.floor((data.dimension / 2))

    # randomly generate the initial population
    for _ in range(population_size):
        individual = generate_individual(data)
        cost, fixed_individual = fix_routes(data, individual)
        population.append((cost, fixed_individual))

    # sort the initial population
    population.sort(key=lambda x: x[0])

    # store the best solution
    min_cost = population[0][0]
    print(f"initial population best: {population[0]}")

    # main loop
    for generation in range(generations):
        next_gen = []

        # elitism
        elite_count = population_size // 10
        next_gen.extend(population[:elite_count])

        # create the next generation
        for _ in range(population_size - elite_count):
            p1, p2 = tournament_selection(population, tournament_size)
            child_seq = crossover(data, p1, p2)  # create a new solution
            child = mutate(data, child_seq, mutation_rate)  # mutate the solution
            child = fix_routes(data, child)  # fix the solution, calculate cost
            next_gen.append(child)

        # sort next_gen and update the population
        population = sorted(next_gen, key=lambda x: x[0])[:population_size]

        # check for new best solution
        if population[0][0] < min_cost:
            min_cost = population[0][0]  # update min_cost
            tracker.append((generation, population[0]))  # store current best solution

    return Solution(population[0][0], population[0][1])
