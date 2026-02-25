import math
import random

from utils.fix_routes import fix_routes
from utils.models import Data


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


def mutate():
    pass
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

def crossover():
    pass


def run(data: Data):
    population = []
    tracker = []  # keep track of optimal solutions

    # scale the population size based on input
    population_size = math.floor((data.dimension / 2))

    # randomly generate the initial population
    for _ in range(population_size):
        individual = generate_individual(data)
        cost, fixed_individual = fix_routes(data, individual)
        population.append((cost, fixed_individual))

    return population
