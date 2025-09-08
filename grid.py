from disk import Disk


class Grid:
    """Define a class for grids"""
    BLUE = (0, 0, 225)
    SPEED = 0

    def __init__(self, start_line, width, height, grid_size):
        self.start_line = start_line
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.temp_disk = []
        self.new_disk = []
        self.disks_width = self.width // self.grid_size
        self.disks_height = (self.height - self.start_line) // self.grid_size
        self.disks = [[] for i in range(self.disks_width)]
        self.total = 0

    def draw_self(self):
        """Draw all disks and lines"""
        noStroke()
        # If there's a falling disk, draw it
        if self.temp_disk:
            self.temp_disk[0].draw_self()
        if self.new_disk:
            self.new_disk[0].draw_self()

        # Draw the still disks
        for col in range(len(self.disks)):
            if self.disks[col]:
                for row in range(len(self.disks[col])):
                    self.disks[col][row].draw_self()

        # Draw the lines of the grid
        stroke(*self.BLUE)
        strokeWeight(10)
        # Draw vertical lines
        for x in range(0, self.width + 1, self.grid_size):
            line(x, self.start_line, x, self.height)
        # Draw horizontal lines
        for y in range(self.start_line, self.height + 1, self.grid_size):
            line(0, y, self.width, y)

    def add_disk(self, disk):
        """Add the disk to stil disks after it falls to bottom"""
        self.disks[disk.x // self.grid_size].append(disk)
        self.SPEED = 0
        self.total += 1
        self.gc.disk_falling = False
        # Change turns after adding a new disk
        self.gc.is_ai_turn, self.gc.is_player_turn =\
            self.gc.is_player_turn, self.gc.is_ai_turn

    def hold_disk(self, x, y, color):
        """When mouse is pressed, hold a disk above"""
        if self.temp_disk:
            self.temp_disk[0] = Disk(x, y, self.grid_size, color)
        else:
            self.temp_disk.append(Disk(x, y, self.grid_size, color))

    def drop_disk(self, x, y, color):
        """Drop a new disk"""
        self.gc.disk_falling = True
        self.new_disk.append(Disk(x, y, self.grid_size, color))

    def update(self):
        """Draw falling and still disks"""
        # Let the new disk fall
        if self.temp_disk:
            self.draw_self()
        if self.new_disk:
            self.draw_self()
            self.SPEED += 1
            self.new_disk[0].y += self.SPEED
            # Add the disk to list when it falls to bottom
            max_y = self.height - self.grid_size // 2\
                - len(self.disks[self.new_disk[0].x // self.grid_size])\
                * self.grid_size
            if self.new_disk[0].y >= max_y:
                self.new_disk[0].y = max_y
                disk = self.new_disk.pop()
                self.add_disk(disk)
                self.check_status(disk)

        # Draw the whole grid
        self.draw_self()

    def check_status(self, disk):
        """Determine whether the game ends"""
        #  Player wins or computer wins
        self.connect_four(disk)
        # A draw
        if self.total == self.disks_width * self.disks_height:
            self.gc.is_a_draw = True

    def connect_four(self, disk):
        count, x1, y1, x2, y2 = self.vertical_four(disk)

        new_count, nx1, ny1, nx2, ny2 = self.horizontal_four(disk)
        if count <= new_count:
            count, x1, y1, x2, y2 = new_count, nx1, ny1, nx2, ny2

        new_count, nx1, ny1, nx2, ny2 = self.left_diagonal_four(disk)
        if count < new_count:
            count, x1, y1, x2, y2 = new_count, nx1, ny1, nx2, ny2

        new_count, nx1, ny1, nx2, ny2 = self.right_diagonal_four(disk)
        if count < new_count:
            count, x1, y1, x2, y2 = new_count, nx1, ny1, nx2, ny2

        if count >= 4:
            if disk.color == 'red':
                self.gc.player_wins = True
            else:
                self.gc.computer_wins = True
            self.gc.is_ai_turn = False
            self.gc.is_player_turn = False

        # Record last move for AI
        if disk.color == "red":
            if self.gc.ai.red_count < count:
                self.gc.ai.red_count = count
                self.gc.ai.red_l_disk = (x1, y1)
                self.gc.ai.red_r_disk = (x2, y2)
        else:
            if self.gc.ai.last_count < count:
                self.gc.ai.last_count = count
                self.gc.ai.l_disk = (x1, y1)
                self.gc.ai.r_disk = (x2, y2)

    def vertical_four(self, disk, count=0):
        """Check if four in a column"""
        m = disk.x // self.grid_size
        n = abs(disk.y - self.height) // self.grid_size
        this_color = disk.color
        down = n
        # Downwards
        while down >= 0:
            if self.disks[m][down].color == this_color:
                count += 1
                down -= 1
            else:
                break
        return count, m, down + 1, m, n

    def horizontal_four(self, disk, count=0):
        """Check if four in a row"""
        left_count = count
        right_count = count
        m = disk.x // self.grid_size
        n = abs(disk.y - self.height) // self.grid_size
        this_color = disk.color
        left = m
        right = m
        # leftwards
        while left >= 0 and len(self.disks[left]) > n:
            if self.disks[left][n].color == this_color:
                left_count += 1
                left -= 1
            else:
                break
        # Rightwards
        while right < self.disks_width and len(self.disks[right]) > n:
            if self.disks[right][n].color == this_color:
                right_count += 1
                right += 1
            else:
                break
        return left_count + right_count - 1, left + 1, n, right - 1, n

    def left_diagonal_four(self, disk, count=0):
        """Check if four in a left diagonal"""
        m = disk.x // self.grid_size
        n = abs(disk.y - self.height) // self.grid_size
        this_color = disk.color
        top_left_count = count
        bottom_right_count = count
        h1 = n
        h2 = n
        left = m
        up = n
        right = m
        down = n
        # top-left
        while left >= 0 and up < self.disks_height\
                and self.disks_height > len(self.disks[left]) > h1:
            if self.disks[left][up].color == this_color:
                top_left_count += 1
                left -= 1
                up += 1
                h1 += 1
            else:
                break
        # bottom-right
        while right < self.disks_width and down >= 0\
                and len(self.disks[right]) > h2 >= 0:
            if self.disks[right][down].color == this_color:
                bottom_right_count += 1
                right += 1
                down -= 1
                h2 -= 1
            else:
                break
        return top_left_count + bottom_right_count - 1, \
            left + 1, up - 1, right - 1, down + 1

    def right_diagonal_four(self, disk, count=0):
        """Check if four in a right diagnol"""
        m = disk.x // self.grid_size
        n = abs(disk.y - self.height) // self.grid_size
        this_color = disk.color
        bottom_left_count = count
        top_right_count = count
        h1 = n
        h2 = n
        left = m
        up = n
        right = m
        down = n
        # bottom-left
        while left >= 0 and down >= 0\
                and len(self.disks[left]) > h1 >= 0:
            if self.disks[left][down].color == this_color:
                bottom_left_count += 1
                left -= 1
                down -= 1
                h1 -= 1
            else:
                break
        # top-right
        while right < self.disks_width and up < self.disks_height\
                and self.disks_height > len(self.disks[right]) > h2:
            if self.disks[right][up].color == this_color:
                top_right_count += 1
                right += 1
                up += 1
                h2 += 1
            else:
                break
        return bottom_left_count + top_right_count - 1, \
            left + 1, down + 1, right - 1, up - 1
