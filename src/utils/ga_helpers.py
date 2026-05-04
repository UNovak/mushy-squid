import random

from utils.models import Data


def new_seq(unvisited: set[int], data: Data, k: int = 3) -> tuple[int, list[int]]:
    cap = data.capacity
    prev = data.depot_id
    seq = []
    cost = 0

    while unvisited:
        available: list[int] = [n for n in unvisited if data.demands[n] <= cap]

        # unvisited nodes truck full
        if unvisited and not available:
            seq.append(data.depot_id)  # end route
            cost += data.distance[prev, data.depot_id]  # update cost
            cap = data.capacity  # reset capacity
            prev = data.depot_id
            continue

        available.sort(key=lambda x: data.distance[prev, x])

        # pick from 'k' closest
        selection_pool = available[:k]
        id = random.choice(selection_pool)

        # update state
        seq.append(id)
        unvisited.remove(id)
        cap -= data.demands[id].item()
        cost += data.distance[prev, id].item()
        prev = id

    return cost, seq  # (int, [])


def validate_seq(data: Data, seq: list[int]) -> tuple[int, list[int]]:
    cap = data.capacity
    prev = data.depot_id
    cost = 0
    res = [data.depot_id]
    visited: set[int] = set()

    # validate sequence
    for i, id in enumerate(seq):
        if id in visited:
            continue  # skip duplicates

        # exceeded capacity - new truck
        if cap - data.demands[id] < 0:
            res.append(data.depot_id)  # return to depot
            cap = data.capacity  # reset capacity
            cost += data.distance[prev, data.depot_id]  # cost of return to depot
            prev = data.depot_id

        # update for next node
        cap -= data.demands[id]  # update capacity
        cost += data.distance[prev, id]  # update cost
        visited.add(id)
        res.append(id)
        prev = id

    unvisited = set(data.ids) - visited
    if unvisited:
        # generate new segment using unvisited nodes
        extra_cost, seq = new_seq(unvisited, data)
        cost += extra_cost
        res += seq

    # close the final route
    cost += data.distance[prev, data.depot_id]
    res.append(data.depot_id)

    return (cost, res)
