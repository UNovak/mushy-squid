from utils.models import Node, ProblemData


def parse_file(file: str) -> ProblemData:
    # data variables
    nodes: dict[int, Node] = {}
    depot_id: int | None = None
    dimension: int
    truck_capacity: int
    dataset_name: str
    edge_type: str

    # section flags
    is_node: bool = False
    is_demand: bool = False
    is_depot: bool = False

    # opeans a readable stream
    with open(file, "r") as stream:
        for line in stream:
            # read one line at a time, remove trailing \n, make a list of strings
            words: list[str] = line.strip().split(" ")

            # skip over empty lines
            if not words:
                continue

            # handle node data
            if is_node and len(words) == 3:
                id, x, y = list(map(int, words))  # cast all strings to a  list of ints
                nodes[id] = Node(x, y)
                continue

            # handle demand data
            if is_demand and len(words) == 2:
                id, demand = list(map(int, words))  # cast all strings to a list of ints
                nodes[id].demand = demand
                continue

            # handle depot data
            if is_depot:
                if words[0] == "-1":  # end of depot list
                    is_depot = False
                elif words[0] != "-1":  # reading node_id of depot
                    depot_id = int(words[0])

                continue

            # parsing headers
            key = words[0]

            # check file data type
            if key == "TYPE":
                if len(words) >= 3 and words[2] != "CVRP":
                    raise ValueError(f"Expected CVRP file type, got: {words[2]}")

            elif key == "NODE_COORD_SECTION":
                is_node = True

            elif key == "DEMAND_SECTION":
                is_demand = True
                is_node = False

            elif key == "DEPOT_SECTION":
                is_depot = True
                is_node = False
                is_demand = False

            elif key == "DIMENSION":
                dimension = int(words[2])

            elif key == "CAPACITY":
                truck_capacity = int(words[2])

            elif key == "NAME":
                dataset_name = words[2]

            elif key == "EDGE_WEIGHT_TYPE":
                edge_type = words[2]

            elif key == "EOF":
                break

        # check for valid depot_id
        assert depot_id is not None

        # create the ProblemData object
        problem_data = ProblemData(
            nodes=nodes,
            depot_id=depot_id,
            truck_capacity=truck_capacity,
            dimension=dimension,
            dataset=dataset_name,
            edge_type=edge_type,
        )

        return problem_data
