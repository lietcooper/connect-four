class Disk:
    """Define a class of yellow and red disks"""
    YELLOW = (225, 225, 0)
    RED = (225, 0, 0)

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw_self(self):
        """Draw a yellow or a red disk"""
        if self.color == "yellow":
            _fill = self.YELLOW
        else:
            _fill = self.RED
        noStroke()
        fill(*_fill)
        circle(self.x, self.y, self.size)
