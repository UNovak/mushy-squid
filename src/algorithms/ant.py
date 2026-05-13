import math
import random

import numpy as np

from utils.helpers import timer
from utils.models import Data, Solution


def pheromone_matrix(size: int) -> np.ndarray:
    """
    returns a 2D matrix
    value - pheromone on route from i to j
    initial value for each field 1.0
    """
    matrix = np.ones((size, size), dtype="f")
    return matrix


def heuristic_matrix(data: Data, beta: float) -> np.ndarray:
    """
    return a 2D matrix
    value: 1/(dist from i to j)^beta
    """
    size = len(data.nodes)
    matrix = np.zeros((size, size), dtype="f")

    # create a matrix mask -> avoid division by 0
    mask = data.distance != 0

    # calculate heuristics where mask == True
    matrix[mask] = (1.0 / data.distance[mask]) ** beta
    return matrix


def score_matrix(pheromones, heuristics, alpha: float) -> np.ndarray:
    """
    return a 2D matrix
    value: (pheromone^alpha) * heuristic
    """

    matrix = (pheromones**alpha) * heuristics
    np.clip(matrix, 0.001, None, out=matrix)
    return matrix.astype("f")


def next_node(current, available, scores) -> int:
    """decides on what node an ant will visit based on distance and pheromone amount"""
    # get the scores of available nodes
    weights = scores[current, available]  # [0.2, 0.5, 0,7]
    total = weights.sum()
    probabilities = [weight / total for weight in weights]  # normalize

    # weights - how likely each node is to be picked
    # k - how many to pick
    return random.choices(available, weights=probabilities, k=1)[0]


def traverse(data: Data, scores) -> tuple[int, list[int]]:
    """
    returns a sequence of nodes as visited by a single ant
    ant = [cost, [1,3,5,4,1,6,7,8,1]]
    """
    unvisited: set[int] = set(data.ids)
    seq: list[int] = [data.depot_id]  # all ants start at depot
    cost = 0

    while unvisited:
        capacity = data.capacity
        available = [id for id in unvisited if data.demands[id] <= capacity]

        while available:
            id = next_node(seq[-1], available, scores)

            cost += data.distance[seq[-1], id]  # update cost
            capacity -= data.demands[id]  # update capacity
            seq.append(id)
            unvisited.remove(id)
            available = [
                node for node in unvisited if node != id and data.demands[node] <= capacity
            ]

        # capacity limit or visited all customers
        cost += data.distance[seq[-1], data.depot_id]
        seq.append(data.depot_id)  # return to depot

    return int(cost), seq


def update_pheromones(data: Data, pheromones: np.ndarray, ants, evaporation=0.2) -> np.ndarray:
    """
    run after all ants have returned
    update pheromone values based on taken routes
    account for pheromone evaporation
    return the updated pheromone matrix
    """

    # evaporate — all pheromones decay
    pheromones *= 1 - evaporation

    # deposit — each ant reinforces its path
    for _, seq in ants:
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i + 1]
            deposit = 10 / data.distance[a, b]  # distance[a,b] symmetric to distance[b,a]
            val = pheromones[a, b] + deposit
            # pheromones[a,b] symmetric to pheromones[b,a]
            pheromones[a, b] = np.clip(val, 0.1, 10.0)
            pheromones[b, a] = np.clip(val, 0.1, 10.0)

    return pheromones


def hybrid(
    data: Data,
    iterations: int = 100,
    alpha: float = 0.5,
    beta: float = 1.0,
    pheromones: np.ndarray | None = None,
    heuristics: np.ndarray | None = None,
) -> tuple[list[tuple[float, list[int]]], np.ndarray, np.ndarray]:
    """returns better half of sorted an and pheromone matrix"""
    size = len(data.nodes)
    ant_count = math.floor(data.dimension / 2)

    # Initialize matrices
    # skip recalculating pheromones if passed as params
    if pheromones is None:
        pheromones = pheromone_matrix(size)

    # skip recalculating heuristics if passed as params
    if heuristics is None:
        heuristics = heuristic_matrix(data, beta)

    # compute score matrix
    scores = score_matrix(pheromones, heuristics, alpha)

    # main loop
    for _ in range(iterations):
        ants: list[tuple[int, list[int]]] = []
        for _ in range(ant_count):
            ant = traverse(data, scores)
            ants.append(ant)

        # update pheromone matrix and the scores matrix
        pheromones = update_pheromones(data, pheromones, ants)
        scores = score_matrix(pheromones, heuristics, alpha)

    # sort ants by cost
    ants.sort(key=lambda x: x[0])
    return ants[: int(len(ants) / 2)], pheromones, heuristics


@timer
def run(data: Data, iterations: int = 100, alpha: float = 0.5, beta: float = 1.0):
    size = len(data.nodes)
    ant_count = math.floor(data.dimension / 2)
    top_ant: tuple[float, list[int]] | None = None
    min_cost = float("inf")

    # Initialize matrices
    pheromones = pheromone_matrix(size)
    heuristics = heuristic_matrix(data, beta)
    scores = score_matrix(pheromones, heuristics, alpha)

    # main loop
    for iteration in range(iterations):
        ants: list[tuple[int, list[int]]] = []
        for _ in range(ant_count):
            ant = traverse(data, scores)  # [cost, [1,2,5,3,1,7,8,4,1]]
            ants.append(ant)

        # update pheromone matrix and the scores matrix
        pheromones = update_pheromones(data, pheromones, ants)
        scores = score_matrix(pheromones, heuristics, alpha)

        # sort ants by cost
        ants.sort(key=lambda x: x[0])

        # check for new best solution
        if ants[0][0] < min_cost:
            min_cost = ants[0][0]  # update min_cost
            top_ant = ants[0]  # update best solution

    # after all iterations return the top ant
    # transform ant to Solution
    assert top_ant is not None

    return Solution(top_ant[0], top_ant[1], "AC")
