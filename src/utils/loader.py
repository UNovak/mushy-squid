import numpy as np
import tsplib95

from utils.models import Data


def get_nodes(problem) -> np.ndarray:
    size = problem.dimension + 1
    nodes = np.zeros((size, 2), dtype="i")
    if problem.node_coords:
        for id, (x, y) in problem.node_coords.items():
            nodes[id] = [x, y]
    return nodes


def get_distance(problem) -> np.ndarray:
    size = problem.dimension + 1
    matrix = np.zeros((size, size), dtype="i")

    for i in range(1, size):
        for j in range(1, size):
            matrix[i, j] = problem.get_weight(i, j)
    return matrix


def load(path: str) -> Data:
    problem = tsplib95.load(path)

    depot_id = problem.depots[0]
    all_ids = list(problem.get_nodes())
    ids = [id for id in all_ids if id != depot_id]

    size = problem.dimension + 1
    demands = np.zeros(size, dtype="i")
    for id in all_ids:
        demands[id] = problem.demands[id]

    nodes = get_nodes(problem)
    distance = get_distance(problem)

    return Data(
        name=problem.name,
        type=problem.type,
        edge_type=problem.edge_weight_type,
        dimension=problem.dimension,
        capacity=problem.capacity,
        depot_id=depot_id,
        ids=ids,
        nodes=nodes,
        demands=demands,
        distance=distance,
    )
