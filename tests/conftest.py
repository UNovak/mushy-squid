import numpy as np
import pytest

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
