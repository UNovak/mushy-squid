import uuid
from dataclasses import dataclass, field


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

    def __repr__(self) -> str:
        nodes_lines = []

        # Limit to the first 10 nodes
        items = list(self.nodes.items())
        for node_id, node in items[:5]:
            nodes_lines.append(f"    {node_id}, [{node.x}, {node.y}, {node.demand}]")

        # Add "..." and the very last node if there are more than 10 nodes
        if len(items) > 5:
            nodes_lines.append("     ...")
            last_node_id, last_node = items[-1]
            nodes_lines.append(
                f"   {last_node_id}, [{last_node.x}, {last_node.y}, {last_node.demand}]"
            )

        nodes_output = "\n".join(nodes_lines)

        return (
            f"Problem data:\n"
            f"  nodes = [\n"
            f"{nodes_output}\n"
            f"  ]\n"
            f"  depot_id = {self.depot_id}\n"
            f"  truck_capacity = {self.truck_capacity}\n"
            f"  dimension = {self.dimension}\n"
            f'  dataset = "{self.dataset}"\n'
            f'  edge_type = "{self.edge_type}"\n'
        )


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
