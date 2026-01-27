import uuid
from dataclasses import dataclass, field

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
    routes: list[list[int]]
    id: str
    """

    cost: int
    routes: list[list[int]]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __repr__(self) -> str:
        return f"[{self.cost}, {self.routes}]"
