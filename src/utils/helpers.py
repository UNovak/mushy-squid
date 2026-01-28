import math

from utils.models import Node, ProblemData


def euc(i: Node, j: Node):
    """returns the eucledean distance between two nodes"""

    xd = i.x - j.x  # x coordinate
    yd = i.y - j.y  # y coordinate
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
