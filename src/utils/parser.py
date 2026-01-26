import numpy as np

from utils.helpers import dist_matrix
from utils.models import Data


def parse_file(file: str) -> Data:
    # data variables
    data = {}
    ids = []
    depot_id = 1

    # section flags
    is_node: bool = False
    is_demand: bool = False
    is_depot: bool = False

    # opens a readable stream
    with open(file, "r") as stream:
        for line in stream:  # read one line at a time
            words: list[str] = line.strip().split()  # remove trailing whitespace and \n

            # skip over empty lines
            if not words:
                continue

            key = words[0].lower().rstrip(":")

            # parse header for data
            if key in ["type", "dimension", "capacity", "name", "edge_weight_type"]:
                data[key] = int(words[-1]) if words[-1].isdigit() else words[-1]
                continue

            # break after data section
            if key == "node_coord_section":
                is_node = True
                break

        # initialize empty arrays
        nodes = np.zeros((data["dimension"] + 1, 2), dtype="i")
        demands = np.zeros(data["dimension"] + 1, dtype="i")

        for line in stream:
            words: list[str] = line.strip().split()
            if not words:
                continue

            if words[0].isdigit():
                # words=['10','180','37']
                if is_node:
                    id, x, y = map(int, words)
                    nodes[id] = [x, y]
                    ids.append(id)

                # words=['8','700']
                if is_demand:
                    id, demand = map(int, words)
                    demands[id] = demand

                if is_depot:
                    depot_id = int(words[0]) if words[0] != "-1" else depot_id

                continue

            key = words[0].lower().rstrip(":")
            if key == "demand_section":
                is_node, is_demand, is_depot = False, True, False
            if key == "depot_section":
                is_node, is_demand, is_depot = False, False, True
            if key == "eof":
                break

        return Data(
            capacity=data["capacity"],
            name=data["name"],
            edge_type=data["edge_weight_type"],
            dimension=data["dimension"],
            type=data["type"],
            depot_id=depot_id,
            ids=ids[1:],
            nodes=nodes,
            demands=demands,
            distance=dist_matrix(nodes),
        )
