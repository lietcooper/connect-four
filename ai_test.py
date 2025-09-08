from game_controller import GameController
from ai import AI
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
        ai.last_count == 0 and
        ai.l_disk == (-1, -1) and
        ai.r_disk == (-1, -1) and
        ai.red_count == 0 and
        ai.red_l_disk == (-1, -1) and
        ai.red_r_disk == (-1, -1)
    )


def test_coordinate_to_length():
    x_length = ai.coordinate_to_length(1)
    y_length = ai.coordinate_to_length(2)
    assert x_length == 150
    assert y_length == 250


def test_win_move():
    gc.ai.last_count = 3
    gc.ai.l_disk = (4, 0)
    gc.ai.r_disk = (4, 2)
    assert gc.ai.win_move() == 4


def test_break_move():
    gc.ai.red_count = 3
    for i in range(3):
        gc.grid.disks[0].append(i)
    gc.ai.red_l_disk = (0, 0)
    gc.ai.red_r_disk = (0, 2)
    assert gc.ai.break_move() == 0


def test_regular_move():
    rand_int = [0, 1, 2, 3, 4, 5, 6]
    assert gc.ai.regular_move() in rand_int
    assert gc.ai.regular_move() in rand_int
    assert gc.ai.regular_move() in rand_int
