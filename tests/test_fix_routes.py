import numpy as np
import pytest

from utils.fix_routes import validate_route
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
    visited = {}

    # valid
    valid = [2, 6, 5]
    status, _, cap, idx = validate_route(valid, visited, sample_data)
    assert status is True
    assert idx == len(valid)
    assert cap == 0

    # local duplicate
    visited = {}
    local_dup = [6, 5, 6]
    status, _, _, idx = validate_route(local_dup, visited, sample_data)
    assert status is False
    assert idx == 2

    # fault at index zero
    visited = {6}
    global_dup = [6, 2, 5]
    status, cost, cap, idx = validate_route(global_dup, visited, sample_data)
    assert status is False
    assert idx == 0
    assert cost == 0
    assert cap == sample_data.capacity

    # fault in the middle
    visited = {6}
    global_dup = [2, 6, 5]
    status, cost, cap, idx = validate_route(global_dup, visited, sample_data)
    assert status is False
    assert idx == 1
    assert cost == 3
    assert cap == 60

    # fault at last index
    visited = {6}
    global_dup = [2, 5, 6]
    status, cost, cap, idx = validate_route(global_dup, visited, sample_data)
    assert status is False
    assert idx == 2
    assert cost == 10
    assert cap == 20

    # exceeded capacity
    visited = {}
    cap_limit = [2, 5, 3]
    status, _, cap, idx = validate_route(cap_limit, visited, sample_data)
    assert status is False
    assert idx == 2
    assert cap == 20
