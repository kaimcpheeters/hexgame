import random
from cell import Cell

DEFAULT_BOARD_COORDS = [
(6, 0),(5, 0),(4, 0),(3, 0),
(2, 1),(3, 1),(4, 1),(5, 1),(6, 1),
(1, 2),(2, 2),(3, 2),(4, 2),(5, 2),(6, 2),
(0, 3),(1, 3),(2, 3),(3, 3),(4, 3),(5, 3),(6, 3),
(6, 4),(0, 4),(1, 4),(2, 4),(3, 4),(4, 4),(5, 4),
(0, 5),(1, 5),(2, 5),(3, 5),(4, 5),(5, 5),(0, 6),
(1, 6),(2, 6),(3, 6),(4, 6),(0, 7),(1, 7),(2, 7),(3, 7)]

def _init_board(coords):
    board = {}
    for coord in coords:
        board[coord] = Cell(coord)
    return board

def _init_resources(board,seed=None):
    count = int(len(board.keys()) / 4)
    resources = (['grain']*count
                 +['wood']*count
                 +['sheep']*count
                 +['ore']*count)
    if seed:
        random.seed(seed)
    random.shuffle(resources)
    for coord, resource in zip(board.keys(),resources):
        board[coord].resource = resource
    return board

def init_board(coords,seed=None):
    '''Initialize board state'''
    board = _init_board(coords)
    board = _init_resources(board,seed)
    return board