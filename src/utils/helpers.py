import math
import random

import numpy as np

from utils.models import Data, Solution


def euc(a: tuple[int, int], b: tuple[int, int]):
    """returns the eucledean distance between two nodes"""

    xd = a[0] - b[0]  # x coordinate
    yd = a[1] - b[1]  # y coordinate
    dist = round(math.sqrt(xd * xd + yd * yd))
    return dist


def dist_matrix(nodes: np.ndarray) -> np.ndarray:
    """returns a 2d matrix of distances between nodes"""
    size = len(nodes)  # n + 1
    matrix = np.zeros((size, size), dtype="i")  # create empty array

    # loop over dist_matrix
    for i in range(1, size):
        for j in range(1, size):
            matrix[i, j] = euc(nodes[i], nodes[j])

    return matrix


def route_cost(data: Data, route: list[int]) -> int:
    """return the total cost of a route"""
    cost = 0
    prev = data.depot_id  # set start to depot
    for id in route:
        cost += int(data.distance[prev, id])
        prev = id  # update last visited

    # add cost from route[-1] to depot
    cost += int(data.distance[prev, data.depot_id])
    return cost


def seq_to_routes(data: Data, seq: list[int]) -> list[list[int]]:
    """takes a single sequence and greedily splits it based on capacity. Returns a set of routes"""
    routes = []
    capacity = data.capacity
    start = 0

    if capacity == 0:
        return []

    for i, id in enumerate(seq):
        if capacity - data.demands[id] < 0:
            routes.append(seq[start:i])
            capacity = data.capacity - data.demands[id]
            start = i
        else:
            capacity -= data.demands[id]

    # always add the last route
    if start < len(seq):
        routes.append(seq[start:])

    return routes


def routes_to_seq():
    pass


def type_print(data: Data, s: Solution) -> None:
    """prints all of the variables and the responding types"""

    id1 = data.ids[0]
    id2 = data.ids[-1]
    id = random.choice(data.ids)
    x, y = data.nodes[id]
    demand = data.demands[id]
    distance = data.distance[id1, id2]
    calculated_demand = 99
    calculated_distance = 99

    print(
        " \n\n ------------------ TYPES -------------------------  \n\n",
        f"random id: {id}, ids[0]: {id1}, ids[-1]: {id2}\n",
        f"nodes -> type(nodes): {type(data.nodes)}, node: {data.nodes[id]} {type(data.nodes[id])}\n",
        f"x:{x} {type(x)}, y:{y} {type(y)}\n",
        f"depot_id -> depot_id: {data.depot_id} {type(data.depot_id)}\n",
        f"euc -> euc_result: {euc(data.nodes[1], data.nodes[2])} {type(euc(data.nodes[1], data.nodes[2]))}\n",
        f"solution -> uuid: {s.id} {type(s.id)}\n",
        f"solution -> cost: {s.cost} {type(s.cost)}\n",
        f"solution -> routes: {s.routes} {type(s.routes)}\n",
        f"solution -> route: {s.routes[0]} {type(s.routes[0])}\n",
        f"solution -> route_id: {s.routes[0][0]} {type(s.routes[0][0])} \n",
        f"demands -> type(demands): {type(data.demands)}, demand:{demand}, {type(demand)}\n",
        f"distance -> type(distance): {type(data.distance)} distance: {distance} {type(distance)}\n",
        f"capacity -> capacity: {data.capacity} {type(data.capacity)}\n",
        f"calculated -> demand before: {calculated_demand} {type(calculated_demand)}\n",
        f"calculated -> distance before: {calculated_distance} {type(calculated_distance)}",
    )

    calculated_demand += demand
    calculated_distance += distance

    print(
        f"calculated_demand += demand -> calculated_demand: {calculated_demand} {type(calculated_demand)}\n",
        f"calculated_distance += distance -> calculated_distance: {calculated_distance} {type(calculated_distance)}\n",
    )
