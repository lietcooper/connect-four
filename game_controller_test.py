from game_controller import GameController
WIDTH = 700
HEIGHT = 700
GRID_SIZE = 100
START_LINE = GRID_SIZE  # the height of click area


def test_constructor():
    global gc
    gc = GameController(START_LINE, WIDTH, HEIGHT, GRID_SIZE, "Lijun")
    assert (
        gc.start_line == 100 and
        gc.width == 700 and
        gc.height == 700
    )


def test_drop_disk():
    gc.drop_disk(150, 50)
    assert len(gc.grid.new_disk) == 1
    disk = gc.grid.new_disk[0]
    assert (
        disk.x == 150 and
        disk.y == 50 and
        disk.color == "red"
    )


def test_hold_disk():
    gc.hold_disk(150, 50)
    assert len(gc.grid.temp_disk) == 1
    disk = gc.grid.new_disk[0]
    assert (
        disk.x == 150 and
        disk.y == 50 and
        disk.color == "red"
    )
