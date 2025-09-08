import random


class AI:
    """A class fot computer moves"""
    def __init__(self, start_line, width, height, grid_size):
        self.start_line = start_line
        self.grid_size = grid_size
        self.rows = (height - start_line) // grid_size
        self.cols = width // grid_size
        self.last_count = 0
        self.l_disk = (-1, -1)  # searched left yellow disk
        self.r_disk = (-1, -1)  # searched right yellow disk
        self.red_count = 0
        self.red_l_disk = (-1, -1)  # searched left red disk
        self.red_r_disk = (-1, -1)  # searched right red disk

    def coordinate_to_length(self, x):
        return x * self.grid_size + self.grid_size // 2

    def move(self):
        """Computer drops a disk"""
        x = self.coordinate_to_length(self.try_move())
        self.gc.grid.drop_disk(x, self.start_line // 2, "yellow")

    def try_move(self):
        """Try different moves"""
        if self.last_count == 3:
            return self.win_move()
        elif self.red_count >= 2:
            return self.break_move()
        else:
            return self.regular_move()

    def win_move(self):
        # if AI is one step from winning
        # Vertically
        if self.l_disk[0] == self.r_disk[0] and\
           self.r_disk[1] + 1 < self.rows:
            return self.l_disk[0]  # return the x
        # Horizontally
        elif self.l_disk[1] == self.r_disk[1]:
            left, right = self.l_disk[0] - 1, self.r_disk[0] + 1
            # If left is empty
            if 0 <= left and len(self.gc.grid.disks[left]) == self.l_disk[1]:
                return left
            # If right is empty
            elif right < self.cols and\
                    len(self.gc.grid.disks[right]) == self.l_disk[1]:
                return right
        # Diagonally
        else:
            left, right = self.l_disk[0] - 1, self.r_disk[1] + 1
            y1, y2 = self.l_disk[1], self.r_disk[1]
            # Right diagonal
            if y1 < y2:
                y1 -= 1
                y2 += 1
                # If left has empty space
                if 0 <= left and 0 <= y1 and\
                   len(self.gc.grid.disks[left]) == self.l_disk[1] - 1:
                    return left
                    # If right has empty space
                elif right < self.cols and y2 < self.rows and\
                        len(self.gc.grid.disks[right]) == self.r_disk[1] + 1:
                    return right
            # Left diagonal
            else:
                y1 += 1
                y2 -= 1
                if left < self.cols and y1 < self.rows and\
                   len(self.gc.grid.disks[left]) == self.l_disk[1] + 1:
                    return left
                elif 0 <= right and 0 <= y2 and\
                        len(self.gc.grid.disks[right]) == self.r_disk[1] - 1:
                    return right
        self.last_count = 0
        return self.regular_move(True)

    def break_move(self):
        # If the player has two in a row, start to intercept
        # Vertically three red disks
        if self.red_l_disk[0] == self.red_r_disk[0]:
            if self.red_count == 3 and\
               len(self.gc.grid.disks[self.red_l_disk[0]]) ==\
               self.red_r_disk[1] + 1:
                self.red_count = 0
                return self.red_l_disk[0]

        # Horizontally three or two with two sides open
        elif self.red_l_disk[1] == self.red_r_disk[1]:
            left, right = self.red_l_disk[0] - 1, self.red_r_disk[0] + 1
            # If two red and not two sides open, take regular move
            if self.red_count == 2 and\
                (
                    0 > left or
                    len(self.gc.grid.disks[left]) != self.red_l_disk[1] or
                    right >= self.cols or
                    len(self.gc.grid.disks[right]) != self.red_r_disk[1]
                    ):
                return self.regular_move()
            # If right is empty
            if right < self.cols and\
               len(self.gc.grid.disks[right]) == self.red_r_disk[1]:
                self.red_count = 0
                return right
            # If left is empty
            elif 0 <= left and \
                    len(self.gc.grid.disks[left]) == self.red_l_disk[1]:
                self.red_count = 0
                return left

        # Diagonally three or two with two sides open
        else:
            left, right = self.red_l_disk[0] - 1, self.red_r_disk[1] + 1
            y1, y2 = self.red_l_disk[1], self.red_r_disk[1]
            # Right diagonal
            if y1 < y2:
                y1 -= 1
                y2 += 1
                # If two red and not two sides open, take regular move
                if self.red_count == 2 and\
                    (
                        0 > left or 0 > y1 or
                        len(self.gc.grid.disks[left]) !=
                        self.red_l_disk[1] - 1 or
                        right >= self.cols or y2 >= self.rows or
                        len(self.gc.grid.disks[right]) !=
                        self.red_r_disk[1] + 1
                        ):
                    return self.regular_move()
                # If left has empty space
                if 0 <= left and 0 <= y1 and\
                   len(self.gc.grid.disks[left]) == self.red_l_disk[1] - 1:
                    self.red_count = 0
                    return left
                    # If right has empty space
                elif right < self.cols and y2 < self.rows and\
                        len(self.gc.grid.disks[right]) ==\
                        self.red_r_disk[1] + 1:
                    self.red_count = 0
                    return right
            # Left diagonal
            else:
                y1 += 1
                y2 -= 1
                # If two red and not two sides open, take regular move
                if self.red_count == 2 and\
                    (
                        0 > left or y1 >= self.rows or
                        len(self.gc.grid.disks[left]) !=
                        self.red_l_disk[1] + 1 or
                        right >= self.cols or 0 > y1 or
                        len(self.gc.grid.disks[right]) !=
                        self.red_r_disk[1] - 1
                        ):
                    return self.regular_move()
                if left < self.cols and y1 < self.rows and\
                   len(self.gc.grid.disks[left]) == self.red_l_disk[1] + 1:
                    self.red_count = 0
                    return left
                elif 0 <= right and 0 <= y2 and\
                        len(self.gc.grid.disks[right]) ==\
                        self.red_r_disk[1] - 1:
                    self.red_count = 0
                    return right
        return self.regular_move()

    def regular_move(self, _break=False):
        if _break and self.red_count >= 2:  # If from win move. try break move
            return self.break_move()
        x = random.randint(0, self.cols - 1)
        while len(self.gc.grid.disks[x]) >= self.rows:
            x = random.randint(0, self.cols - 1)
        return x
