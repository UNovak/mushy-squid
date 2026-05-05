import uuid
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass(frozen=True, slots=True)
class Data:
    """
    type: str
    name: str
    edge_type: str
    dimension: int
    capacity: int
    depot_id: int
    ids: list[int]
    nodes: arr[id] = x,y
    demands: arr[id]= demand
    distance: arr[from,to]
    """

    type: str
    name: str
    edge_type: str
    dimension: int  # customers + depot
    capacity: int  # capacity of one truck
    depot_id: int
    ids: list[int] = field(repr=False)
    nodes: np.ndarray  # size(n+1,2)
    demands: np.ndarray  # size(n+1)
    distance: np.ndarray  # size(n+1,n+1)


@dataclass
class Solution:
    """
    cost: int
    seq: list[int]
    algorithm: str | None
    id: str
    """

    cost: int
    seq: list[int]
    algorithm: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __repr__(self) -> str:
        return f"cost={self.cost}, seq={self.seq}, algorithm={self.algorithm}"
