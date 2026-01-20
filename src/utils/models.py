from dataclasses import dataclass


@dataclass
class Node:
    """
    x: int
    y: int
    demand: int
    """

    x: int
    y: int
    demand: int = 0


@dataclass
class ProblemData:
    """
    nodes: dict[node_id,[id,x,y,demand]]
    depot_id: int
    truck_capacity: int
    dimension: int
    dataset: str
    edge_type: str
    """

    nodes: dict[int, Node]
    depot_id: int
    truck_capacity: int
    dimension: int
    dataset: str
    edge_type: str
