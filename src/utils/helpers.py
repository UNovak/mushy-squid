import math

import numpy as np


def euc(a: tuple[int, int], b: tuple[int, int]):
    """returns the eucledean distance between two nodes"""

    xd = a[0] - b[0]  # x coordinate
    yd = a[1] - b[1]  # y coordinate
    dist = round(math.sqrt(xd * xd + yd * yd))
    return dist


def dist_matrix(nodes: np.ndarray) -> np.ndarray:
    """returns a 2d matrix of distances between nodes"""
    size = len(nodes)  # n + 1
    matrix = np.zeros((size, size), dtype="i")  # create empty array

    # loop over dist_matrix
    for i in range(1, size):
        for j in range(1, size):
            matrix[i, j] = euc(nodes[i], nodes[j])

    return matrix
