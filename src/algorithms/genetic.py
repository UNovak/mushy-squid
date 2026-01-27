import math
import random

from utils.models import ProblemData


def run(data: ProblemData, dist_matrix):
    # extract the needed data
    nodes = data.nodes
    capacity = data.truck_capacity
    depot_id = data.depot_id

    # generate a random population
    def init():
        """returns a randomly generated population"""
        # scale the population size based on input
        population_size = math.floor((data.dimension - 1) / 10) * 2

        # generate a list of all node ids
        ids = [k for k in nodes.keys() if k != depot_id]
        population = []

        for _ in range(population_size):
            unvisited = set(ids)
            routes = []

            while unvisited:
                current_capacity = capacity
                possible_customer = list(unvisited)
                route = []

                while possible_customer:
                    id = random.choice(possible_customer)
                    current_capacity -= nodes[id].demand
                    route.append(id)
                    unvisited.remove(id)

                    # update possible customers based on unvisited nodes and remaining truck capacity
                    possible_customer = [
                        id for id in unvisited if nodes[id].demand <= current_capacity
                    ]

                # no possible next customer
                current_capacity = capacity
                routes.append(route)

            # all customers visited
            population.append(routes)

        return population

    population = init()
