from utils.models import Data


def validate_route(route, visited, data: Data) -> tuple[bool, int, int, int]:
    locals: set[int] = set()
    cap = data.capacity
    cost = 0
    prev = data.depot_id
    for idx, id in enumerate(route):
        if cap - data.demands[id] < 0:
            return False, cost, cap, idx

        if id in visited or id in locals:
            return False, cost, cap, idx

        # no errors, update state
        locals.add(id)
        cap -= data.demands[id].item()
        cost += data.distance[prev, id].item()
        prev = id

    cost += data.distance[prev, data.depot_id].item()
    return True, cost, cap, len(route)


def strip_route(route: list[int], idx: int):
    good_seg = route[:idx]
    bad_seg = route[idx:]
    return good_seg, bad_seg


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
