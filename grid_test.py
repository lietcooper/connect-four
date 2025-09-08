from disk import Disk
from grid import Grid
WIDTH = 700
HEIGHT = 700
GRID_SIZE = 100
START_LINE = GRID_SIZE  # the height of click area


def test_constructor():
    global grid
    grid = Grid(START_LINE, WIDTH, HEIGHT, GRID_SIZE)
    assert (
        grid.start_line == 100 and
        grid.width == 700 and
        grid.height == 700 and
        grid.grid_size == 100 and
        not grid.temp_disk and
        not grid.new_disk and
        grid.disks_width == 7 and
        grid.disks_height == 6 and
        len(grid.disks) == 7 and
        len(grid.disks[0]) == 0 and
        grid.total == 0
    )


def test_hold_disk():
    grid.hold_disk(150, 50, "red")
    assert len(grid.temp_disk) == 1
    disk = grid.temp_disk[0]
    assert (
        disk.x == 150 and
        disk.y == 50 and
        disk.color == "red"
    )


def test_drop_disk():
    grid.hold_disk(150, 50, "yellow")
    assert len(grid.temp_disk) == 1
    disk = grid.temp_disk[0]
    assert (
        disk.x == 150 and
        disk.y == 50 and
        disk.color == "yellow"
    )


def test_connect_four():
    for x in range(0, 4):
        for y in range(0, 4):
            grid.disks[x].append(Disk(x * 100 + 50, 650 - y * 100,
                                 GRID_SIZE, "red"))

    disk1 = Disk(50, 350, GRID_SIZE, "red")
    disk2 = Disk(150, 450, GRID_SIZE, "red")
    disk3 = Disk(250, 550, GRID_SIZE, "red")
    disk4 = Disk(150, 550, GRID_SIZE, "red")
    count, x1, y1, x2, y2 = grid.vertical_four(disk1)
    assert (
        count == 4 and
        x1 == 0 and
        y1 == 0 and
        x2 == 0 and
        y2 == 3
    )
    count, x1, y1, x2, y2 = grid.horizontal_four(disk2)
    assert (
        count == 4 and
        x1 == 0 and
        y1 == 2 and
        x2 == 3 and
        y2 == 2
    )
    count, x1, y1, x2, y2 = grid.left_diagonal_four(disk3)
    assert (
        count == 4 and
        x1 == 0 and
        y1 == 3 and
        x2 == 3 and
        y2 == 0
    )
    count, x1, y1, x2, y2 = grid.right_diagonal_four(disk4)
    assert (
        count == 4 and
        x1 == 0 and
        y1 == 0 and
        x2 == 3 and
        y2 == 3
    )
