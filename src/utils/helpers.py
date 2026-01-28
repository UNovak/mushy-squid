import math

from utils.models import Node


def euc(i: Node, j: Node):
    """returns the eucledean distance between two nodes"""

    xd = i.x - j.x  # x coordinate
    yd = i.y - j.y  # y coordinate
    dist = round(math.sqrt(xd * xd + yd * yd))
    return dist
