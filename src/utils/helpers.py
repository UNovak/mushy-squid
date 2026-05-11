from functools import wraps
from time import time

from utils.models import Data, Solution


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
