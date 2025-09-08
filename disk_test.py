from disk import Disk


def test_constructor():
    x = 150
    y = 650
    size = 100
    color = "red"
    disk = Disk(x, y, size, color)
    assert (
        disk.x == 150 and
        disk.y == 650 and
        disk.size == 100 and
        disk.color == "red"
    )
