import math

from utils.models import ProblemData


def euc(a: tuple[int, int], b: tuple[int, int]):
    """returns the eucledean distance between two nodes"""

    xd = a[0] - b[0]  # x coordinate
    yd = a[1] - b[1]  # y coordinate
    dist = round(math.sqrt(xd * xd + yd * yd))
    return dist


def all_distances(data: ProblemData) -> dict[int, dict[int, int]]:
    """returns a dictionary of all distances"""
    ids = list(data.nodes.keys())
    result = {}

    for key in ids:
        tmp = {}
        for id in ids:
            tmp[id] = euc(data.nodes[id], data.nodes[key])

        result[key] = tmp

    return result
