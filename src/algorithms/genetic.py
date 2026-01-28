import math
import random

from utils.models import Data


def run(data: Data):
    # extract the needed data
    capacity = data.capacity
    depot_id = data.depot_id

    def init():
        """returns a randomly generated population"""
        # scale the population size based on input
        population_size = math.floor((data.dimension - 1) / 10) * 2

        population = []

        for _ in range(population_size):
            unvisited = set(data.ids)  # get all customer node_ids
            routes = []

            while unvisited:
                current_capacity = capacity
                possible_customer = list(unvisited)
                route = []  # path of one vehicle

                while possible_customer:
                    id = random.choice(possible_customer)  # pick a random node
                    current_capacity -= data.demands[id]  # update truck capacity
                    route.append(id)  # add id to path
                    unvisited.remove(id)  # mark node as visited, remove it from set

                    # update possible customers based on unvisited nodes and remaining truck capacity
                    possible_customer = [
                        id for id in unvisited if data.demands[id] <= current_capacity
                    ]

                # unvisited nodes, no possible customer
                routes.append(route)

            # all customers visited
            population.append(routes)

        return population

    population = init()
