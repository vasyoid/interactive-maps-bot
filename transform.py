import os
import numpy as np

from typing import List, Tuple


class Transform:

    def __init__(self):
        self._mat = _calculate_matrix()

    def apply(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        p = np.matmul(self._mat, [pos[0], pos[1], 1])
        return int(p[0]), int(p[1])


def _get_init_points() -> List[List[List[float]]]:
    with open(os.path.join(os.getcwd(), "res", "init.txt")) as file:
        return [[[float(x) for x in next(file).split()] for _ in range(3)] for _ in range(2)]


def _build_equation(src: List[List[float]], dst: List[List[float]]) -> Tuple[np.ndarray, np.ndarray]:
    a = np.array((
        (src[0][0], src[0][1], 1, 0,         0,         0),
        (0,         0,         0, src[0][0], src[0][1], 1),
        (src[1][0], src[1][1], 1, 0,         0,         0),
        (0,         0,         0, src[1][0], src[1][1], 1),
        (src[2][0], src[2][1], 1, 0,         0,         0),
        (0,         0,         0, src[2][0], src[2][1], 1),
    ))
    b = np.array(dst).flatten()
    return a, b


def _calculate_matrix() -> np.ndarray:
    src, dst = _get_init_points()
    a, b = _build_equation(src, dst)
    x = np.linalg.solve(a, b)
    return np.array((
        (x[0], x[1], x[2]),
        (x[3], x[4], x[5]),
        (0, 0, 1)
    ))
