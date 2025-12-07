import random
import copy


class AI:
    """A class for computer moves using minimax with alpha-beta pruning"""
    def __init__(self, start_line, width, height, grid_size):
        self.start_line = start_line
        self.grid_size = grid_size
        self.rows = (height - start_line) // grid_size
        self.cols = width // grid_size
        self.max_depth = 6  # Depth limit for minimax search

    def coordinate_to_length(self, x):
        return x * self.grid_size + self.grid_size // 2

    def move(self):
        """Computer drops a disk"""
        x = self.coordinate_to_length(self.try_move())
        self.gc.grid.drop_disk(x, self.start_line // 2, "yellow")

    def try_move(self):
        """Use minimax algorithm to find the best move"""
        best_col, _ = self.minimax(self.gc.grid.disks, self.max_depth, True, float('-inf'), float('inf'))
        return best_col

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning
        Returns (best_column, score)
        """
        # Check for terminal states
        is_terminal, score = self.is_terminal(board)
        if depth == 0 or is_terminal:
            return None, score

        valid_moves = self.get_valid_moves(board)

        if maximizing_player:  # AI's turn (yellow)
            max_eval = float('-inf')
            best_col = random.choice(valid_moves)  # Default to random valid move

            for col in valid_moves:
                board_copy = self.make_move(board, col, "yellow")
                _, eval_score = self.minimax(board_copy, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return best_col, max_eval
        else:  # Player's turn (red)
            min_eval = float('inf')
            best_col = random.choice(valid_moves)  # Default to random valid move

            for col in valid_moves:
                board_copy = self.make_move(board, col, "red")
                _, eval_score = self.minimax(board_copy, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return best_col, min_eval

    def is_terminal(self, board):
        """Check if the game is over and return the score"""
        # Check for win conditions
        if self.check_win(board, "yellow"):
            return True, 1000000  # AI wins
        if self.check_win(board, "red"):
            return True, -1000000  # Player wins

        # Check for draw (board full)
        if self.is_board_full(board):
            return True, 0  # Draw

        return False, 0  # Game continues

    def check_win(self, board, color):
        """Check if the given color has won"""
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.get_cell(board, row, col + i) == color for i in range(4)):
                    return True

        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if all(self.get_cell(board, row + i, col) == color for i in range(4)):
                    return True

        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.get_cell(board, row + i, col + i) == color for i in range(4)):
                    return True

        # Check diagonal (negative slope)
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if all(self.get_cell(board, row + i, col - i) == color for i in range(4)):
                    return True

        return False

    def get_cell(self, board, row, col):
        """Get the color at a specific position, or None if empty"""
        if col < 0 or col >= self.cols or row < 0:
            return None
        if len(board[col]) > row:
            return board[col][row].color
        return None

    def is_board_full(self, board):
        """Check if the board is completely full"""
        return all(len(col) == self.rows for col in board)

    def get_valid_moves(self, board):
        """Get list of valid columns to play in"""
        return [col for col in range(self.cols) if len(board[col]) < self.rows]

    def make_move(self, board, col, color):
        """Make a move on a copy of the board and return the new board"""
        board_copy = copy.deepcopy(board)
        # Create a simple disk object
        disk = DiskObject(color)
        board_copy[col].append(disk)
        return board_copy


class DiskObject:
    """A simple disk object for the AI simulation"""
    def __init__(self, color):
        self.color = color

    def evaluate_board(self, board):
        """Evaluate the current board position for the AI"""
        if self.check_win(board, "yellow"):
            return 1000000
        if self.check_win(board, "red"):
            return -1000000
        if self.is_board_full(board):
            return 0

        score = 0
        # Evaluate center column preference
        center_col = self.cols // 2
        center_count = len(board[center_col])
        score += center_count * 3

        # Evaluate all possible 4-piece windows
        score += self.evaluate_window(board)

        return score

    def evaluate_window(self, board):
        """Evaluate all possible 4-piece windows on the board"""
        score = 0

        # Horizontal windows
        for row in range(self.rows):
            for col in range(self.cols - 3):
                window = [self.get_cell(board, row, col + i) for i in range(4)]
                score += self.evaluate_window_score(window, "yellow") * 1
                score += self.evaluate_window_score(window, "red") * -1

        # Vertical windows
        for row in range(self.rows - 3):
            for col in range(self.cols):
                window = [self.get_cell(board, row + i, col) for i in range(4)]
                score += self.evaluate_window_score(window, "yellow") * 1
                score += self.evaluate_window_score(window, "red") * -1

        # Diagonal windows (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                window = [self.get_cell(board, row + i, col + i) for i in range(4)]
                score += self.evaluate_window_score(window, "yellow") * 1
                score += self.evaluate_window_score(window, "red") * -1

        # Diagonal windows (negative slope)
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                window = [self.get_cell(board, row + i, col - i) for i in range(4)]
                score += self.evaluate_window_score(window, "yellow") * 1
                score += self.evaluate_window_score(window, "red") * -1

        return score

    def evaluate_window_score(self, window, color):
        """Evaluate a 4-piece window for a given color"""
        score = 0
        opp_color = "red" if color == "yellow" else "yellow"

        if window.count(color) == 4:
            score += 100
        elif window.count(color) == 3 and window.count(None) == 1:
            score += 10
        elif window.count(color) == 2 and window.count(None) == 2:
            score += 2

        if window.count(opp_color) == 3 and window.count(None) == 1:
            score -= 80  # Prioritize blocking opponent

        return score