from typing import List

import random


def matrix(
        rows: int,
        cols: int, 
        min_value: int = -100, 
        max_value: int = 100
) -> List[List[int]]:
    """Generate a random matrix with the specified number of rows and columns.

    Args:
        rows -- int: Row dimension
        cols -- int: Column dimension
        min_value -- int: Min cell value [default: -100]
        max_value -- int: Max cell value [default: 100]

    Returns:
        List[List[int]]
    """
    matrix = [[random.randint(min_value, max_value) for _ in range(cols)] for _ in range(rows)]
    return matrix


def square_matrix(
        n: int,
        min_value: int = -100, 
        max_value: int = 100
) -> List[List[int]]:
    """Generate a random square matrix with the specified number of rows and columns.

    Args:
        n -- int: Dimension
        min_value -- int: Min cell value [default: -100]
        max_value -- int: Max cell value [default: 100]

    Returns:
        List[List[int]]
    """
    return matrix(rows=n, cols=n, min_value=min_value, max_value=max_value)
