from game_controller import GameController
from ai import AI, DiskObject
WIDTH = 700
HEIGHT = 700
GRID_SIZE = 100
START_LINE = GRID_SIZE  # the height of click area
gc = GameController(START_LINE, WIDTH, HEIGHT, GRID_SIZE, "Lijun")


def test_constructor():
    global ai
    ai = AI(START_LINE, WIDTH, HEIGHT, GRID_SIZE)
    assert (
        ai.start_line == 100 and
        ai.grid_size == 100 and
        ai.rows == 6 and
        ai.cols == 7 and
        ai.max_depth == 6
    )


def test_coordinate_to_length():
    x_length = ai.coordinate_to_length(1)
    y_length = ai.coordinate_to_length(2)
    assert x_length == 150
    assert y_length == 250


def reset_board():
    gc.grid.disks = [[] for _ in range(gc.grid.disks_width)]
    gc.grid.total = 0


def add_disk(column, color):
    gc.grid.disks[column].append(DiskObject(color))
    gc.grid.total += 1


def test_try_move_finds_winning_play():
    reset_board()
    for column in range(3):
        add_disk(column, "yellow")
    add_disk(0, "red")
    add_disk(1, "red")
    assert gc.ai.try_move() == 3


def test_try_move_blocks_player():
    reset_board()
    for column in range(3):
        add_disk(column, "red")
    add_disk(4, "yellow")
    assert gc.ai.try_move() == 3
