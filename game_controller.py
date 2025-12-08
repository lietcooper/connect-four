from grid import Grid
from ai import AI
from score_keeper import ScoreKeeper


class GameController:
    """To control the flow of the game and action of the player and ai"""
    WHITE = (255, 255, 255)

    def __init__(self, start_line, width, height, grid_size, name, max_depth=6):
        self.start_line = start_line
        self.width = width
        self.height = height
        self.grid = Grid(start_line, width, height, grid_size)
        self.grid.gc = self
        self.ai = AI(start_line, width, height, grid_size, max_depth)
        self.ai.gc = self
        self.disk_falling = False
        self.is_player_turn = True
        self.is_ai_turn = False
        self.is_a_draw = False
        self.player_wins = False
        self.computer_wins = False
        self.cd = 0  # count down for ai move
        self.TEXT_SIZE = 75
        self.TEXT_POS = (self.width/4, self.height/2)
        self.score_keeper = ScoreKeeper(name)
        self.game_stop = False

    def drop_disk(self, x, y):
        """Drop a disk after a click in the upper area"""
        if self.is_player_turn:
            self.grid.drop_disk(x, y, "red")

    def hold_disk(self, x, y):
        if self.is_player_turn:
            self.grid.hold_disk(x, y, "red")

    def update(self):
        self.grid.update()
        # When it's computer's turn and the player's ball has dropped
        if self.is_ai_turn and not self.disk_falling:
            self.cd += 1
            if self.cd == 50:
                self.ai.move()
                self.cd = 0
        self.display_end_text()
        self.save_score()

    def save_score(self):
        if not self.game_stop:
            if self.player_wins:
                self.score_keeper.save_score()
                self.game_stop = True
            if self.computer_wins or self.is_a_draw:
                self.score_keeper.save_score(False)
                self.game_stop = True

    def display_end_text(self):
        if self.is_a_draw:
            fill(*self.WHITE)
            textSize(self.TEXT_SIZE)
            text("IT'S A DRAW", *self.TEXT_POS)
        if self.player_wins:
            fill(*self.WHITE)
            textSize(self.TEXT_SIZE)
            text("RED WINS!", *self.TEXT_POS)
        if self.computer_wins:
            fill(*self.WHITE)
            textSize(self.TEXT_SIZE)
            text("YELLOW WINS!", *self.TEXT_POS)

