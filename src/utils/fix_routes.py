from utils.models import Data


def validate_route(route, visited, data: Data) -> tuple[bool, int, int, int]:
    locals: set[int] = set()
    capacity = data.capacity
    cost = 0
    prev = data.depot_id
    for index, id in enumerate(route):
        if capacity - data.demands[id] < 0:
            return False, cost, capacity, index

        if id in visited or id in locals:
            return False, cost, capacity, index

        # no errors, update values
        locals.add(id)
        capacity -= data.demands[id].item()
        cost += data.distance[prev, id].item()
        prev = id

    cost += data.distance[prev, data.depot_id]
    return True, cost, capacity, len(route)


def strip_route(route: list[int], index: int):
    good_seg = route[:index]
    bad_seg = route[index:]
    return good_seg, bad_seg

