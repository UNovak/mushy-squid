import numpy as np
import pytest

from utils.fix_routes import (
    complete_seg,
    find_lowest_cost,
    generate_new_route,
    strip_route,
    validate_route,
)
from utils.models import Data


@pytest.fixture
def sample_data() -> Data:
    return Data(
        capacity=100,
        name="test",
        edge_type="EUC_2D",
        dimension=4,
        type="CVRP",
        depot_id=1,
        ids=[2, 3, 4, 5, 6],
        nodes=np.array([[0, 0], [0, 0], [0, 3], [4, 0], [3, 4], [7, 3], [2, 2]], dtype="i"),
        demands=np.array(
            [
                0,
                0,  # 1
                40,  # 2
                70,  # 3
                50,  # 4
                40,  # 5
                20,  # 6
            ],
            dtype="i",
        ),
        distance=np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 4, 5, 8, 3],
            [0, 3, 0, 5, 3, 7, 2],
            [0, 4, 5, 0, 4, 4, 3],
            [0, 5, 3, 4, 0, 4, 2],
            [0, 8, 7, 4, 4, 0, 5],
            [0, 3, 2, 3, 2, 5, 0],
        ]),
    )


def test_route_validation(sample_data: Data):
    visited = {}  # setup

    # valid
    valid = [2, 6, 5]
    status, _, cap, idx = validate_route(valid, visited, sample_data)
    assert status is True
    assert idx == len(valid)
    assert cap == 0

    # exceeded capacity
    cap_limit = [2, 5, 3]
    status, _, cap, idx = validate_route(cap_limit, visited, sample_data)
    assert status is False
    assert idx == 2
    assert cap == 20

    # local duplicate
    local_dup = [6, 5, 6]
    status, _, _, idx = validate_route(local_dup, visited, sample_data)
    assert status is False
    assert idx == 2

    visited = {6}  # setup

    # fault at index zero
    dup_zero = [6, 2, 5]
    status, cost, cap, idx = validate_route(dup_zero, visited, sample_data)
    assert status is False
    assert idx == 0
    assert cost == 0
    assert cap == sample_data.capacity

    # fault in the middle
    dup_middle = [2, 6, 5]
    status, cost, cap, idx = validate_route(dup_middle, visited, sample_data)
    assert status is False
    assert idx == 1
    assert cost == 3
    assert cap == 60

    # fault at last index
    dup_end = [2, 5, 6]
    status, cost, cap, idx = validate_route(dup_end, visited, sample_data)
    assert status is False
    assert idx == 2
    assert cost == 10
    assert cap == 20


def test_strip_route():
    # setup
    route = [2, 5, 6]

    # split at index zero
    good, bad = strip_route(route, 0)
    assert good == []
    assert bad == [2, 5, 6]

    # split in the middle
    good, bad = strip_route(route, 1)
    assert good == [2]
    assert bad == [5, 6]

    # split at the end
    good, bad = strip_route(route, 2)
    assert good == [2, 5]
    assert bad == [6]


def test_find_lowest_cost(sample_data: Data):
    last = 5  # 5-1 d=8 c=60

    # same cost
    available = [6]  # 5-6=5 6-1=3
    id, cost = find_lowest_cost(last, available, sample_data)
    assert cost == 5
    assert id == 6

    # full truck
    available = []
    id, cost = find_lowest_cost(last, available, sample_data)
    assert cost == 0
    assert id == sample_data.depot_id

    # both nodes work, 2nd one adds less extra cost
    available = [2, 4]  # 5-2-1 d=10 c=20, 5-4-1 d=9 c=10
    id, extra_cost = find_lowest_cost(last, available, sample_data)
    assert extra_cost == 4
    assert id == 4


def test_complete_seg(sample_data: Data):
    # setup
    seg = [2, 6]
    cost, cap = 5, 40

    # no free nodes
    free = set()
    total_cost, complete = complete_seg(cost, cap, seg, free, sample_data)
    assert total_cost == 8  # 1-2-6-1
    assert complete == [2, 6]
    assert not free

    # free nodes but over capacity
    free = {3}
    total_cost, complete = complete_seg(cost, cap, seg, free, sample_data)
    assert total_cost == 8
    assert complete == [2, 6]
    assert free == {3}

    # valid completion one possible id
    free = {5}
    total_cost, complete = complete_seg(cost, cap, seg, free, sample_data)
    assert total_cost == 18  # 1-2-6-5-1 -> 3+2+5+8
    assert complete == [2, 6, 5]
    assert not free

    # valid completion
    free = {3, 4, 5}
    total_cost, complete = complete_seg(cost, cap, seg, free, sample_data)
    assert total_cost == cost + 13
    assert complete == [2, 6, 5]
    assert free == {3, 4}


def test_generate_new_route(sample_data: Data):

    # use all available nodes
    unvisited = {5, 2, 6}
    cost, route = generate_new_route(unvisited, sample_data, 1)
    assert route == [2, 6, 5]
    assert cost == 18
    assert not unvisited

    # empty unvisited
    unvisited = set()
    cost, route = generate_new_route(unvisited, sample_data, k=1)
    assert route == []
    assert cost == 0

    # leftover nodes
    sample_data = dataclasses.replace(sample_data, capacity=110)
    unvisited = {2, 6, 5, 4}
    cost, route = generate_new_route(unvisited, sample_data, 1)
    assert route == [2, 6, 4]
    assert cost == 12
    assert unvisited == {5}

    # all demands > capacity
    sample_data = dataclasses.replace(sample_data, capacity=10)
    unvisited = {2, 3, 4}  # demands > 10
    cost, route = generate_new_route(unvisited, sample_data, k=1)
    assert route == []
    assert cost == 0
    assert unvisited == {2, 3, 4}
