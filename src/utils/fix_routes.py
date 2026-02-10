import copy
import random

from utils.models import Data


def validate_route(route: list[int], visited: set[int], data: Data) -> tuple[bool, int, int, int]:
    local_visited: set[int] = set()
    cap = data.capacity
    cost = 0
    prev = data.depot_id
    for idx, id in enumerate(route):
        if cap - data.demands[id] < 0:
            return False, cost, cap, idx

        if id in visited or id in local_visited:
            return False, cost, cap, idx

        # no errors, update state
        local_visited.add(id)
        cap -= data.demands[id].item()
        cost += data.distance[prev, id].item()
        prev = id

    cost += data.distance[prev, data.depot_id].item()
    return True, cost, cap, len(route)


def strip_route(route: list[int], idx: int):
    good_seg = route[:idx]
    bad_seg = route[idx:]
    return good_seg, bad_seg


def generate_new_route(unvisited: set[int], data: Data, k: int = 3) -> tuple[int, list[int]]:
    cap = data.capacity
    prev = data.depot_id
    route = []
    cost = 0

    while True:
        available: list[int] = [n for n in unvisited if data.demands[n] <= cap]
        if not available:
            break

        available.sort(key=lambda x: data.distance[prev, x])

        # pick from 'k' closest
        selection_pool = available[:k]
        id = random.choice(selection_pool)

        # update state
        route.append(id)
        unvisited.remove(id)
        cap -= data.demands[id].item()
        cost += data.distance[prev, id].item()
        prev = id

    cost += data.distance[prev, data.depot_id].item()
    return cost, route


def complete_seg(
    cost: int, cap: int, seg: list[int], free: set[int], data: Data
) -> tuple[int, list[int]]:
    current_cap = cap
    complete = copy.copy(seg)
    total_cost = cost

    while True:
        available = [n for n in free if data.demands[n] <= current_cap]
        if not available:
            break

        id, extra_cost = find_lowest_cost(complete[-1], available, data)
        if id == data.depot_id:  # no better option
            break

        # update state
        current_cap -= data.demands[id]
        total_cost += extra_cost
        free.remove(id)
        complete.append(id)

    # truck full or no way to improve
    total_cost += data.distance[complete[-1], data.depot_id]
    return int(total_cost), complete


def find_lowest_cost(start: int, available_ids: list[int], data: Data) -> tuple[int, int]:
    min_delta = float("inf")
    best_id = data.depot_id
    old_cost = data.distance[start, best_id]

    # loop over all ids that fit the current capacity
    for id in available_ids:
        new_cost = data.distance[start, id] + data.distance[id, data.depot_id]
        delta = new_cost - old_cost

        if delta < min_delta:
            min_delta = delta
            best_id = id

    if best_id == data.depot_id:
        return best_id, 0

    extra_cost = data.distance[start, best_id].item()
    return best_id, extra_cost


def fix_routes(data: Data, routes: list[list[int]]):
    visited: set[int] = set()
    free: set[int] = set()
    incomplete: list[tuple[int, int, list[int]]] = []
    total_cost = 0
    valid = []

    for route in routes:
        status, cost, cap, idx = validate_route(route, visited, data)
        if status:
            total_cost += cost
            valid.append(route)
            visited.update(route)

        else:
            good_seg, bad_seg = strip_route(route, idx)

            for id in bad_seg:
                if id not in visited:
                    free.add(id)

            if good_seg:
                # cache the good part for later
                incomplete.append((cost, cap, good_seg))
                visited.update(good_seg)

    # first try to fill the already used trucks
    if incomplete:
        for cost, cap, seg in incomplete:
            complete_cost, complete = complete_seg(cost, cap, seg, free, data)
            total_cost += complete_cost
            valid.append(complete)

    # make a set containing never visited nodes and nods we removed from invalid routes
    unvisited = (set(data.ids) - visited) | free
    while unvisited:
        cost, route = generate_new_route(unvisited, data)
        if route:
            total_cost += cost
            valid.append(route)
        else:
            break

    return total_cost, valid
