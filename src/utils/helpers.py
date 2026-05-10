import math
from functools import wraps
from time import time

import numpy as np

from utils.models import Data, Solution


def euc(a: tuple[int, int], b: tuple[int, int]):
    """returns the euclidean distance between two nodes"""

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


def validate_solution(data: Data, solution: Solution) -> Solution:
    seq_cost = solution.cost
    seq = solution.seq
    visited = set()
    cost = 0
    cap = data.capacity
    prev = data.depot_id

    for id in seq:
        if id != data.depot_id:
            assert id not in visited, f"Duplicated customer: {id}"
            assert data.demands[id] <= cap, f"Capacity violated at node {id}"
            visited.add(id)
            cap -= data.demands[id]
        else:
            cap = data.capacity
        cost += data.distance[prev, id]
        prev = id

    assert visited == set(data.ids), f"Unvisited nodes: {set(data.ids) - visited}"
    assert round(cost) == round(seq_cost), f"Cost mismatch: stored={seq_cost}, computed={cost}\n"

    return solution


def timer(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"{func.__module__}.{func.__name__!r} executed in {(t2 - t1):.6f}s")
        return result

    return wrap_func
