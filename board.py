import numpy as np
from commons import *


class Board:
    def __init__(self):
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.column = 0

    def is_valid_move(self, column):
        """A move is valid if the top row of the column is empty."""
        return self.grid[0][column] == 0

    def make_move(self, col):
        """Makes a move in the specified column in the first available row.

        Args:
            col (int): The column to make the move in.

        Returns:
            int: The row the move was made in, or -1 if the move is invalid.
        """
        if not self.is_valid_move(col):
            return -1

        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = self.current_player
                self.current_player = 3 - self.current_player  # Change player
                return row

    def is_gameover(self):
        """Checks if the game is over."""
        return self.get_game_result() is not None

    def get_game_result(self):
        """Checks if the game is over and returns the result.

        Returns:
            int: The result of the game, or None if the game is not over.
        """

        # Check for 4 in a row
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if self._check_line([(row, col + i) for i in range(4)]):
                    return PLAYER1 if self.grid[row][col] == PLAYER1 else PLAYER2

        # Check for 4 in a column
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if self._check_line([(row + i, col) for i in range(4)]):
                    return PLAYER1 if self.grid[row][col] == PLAYER1 else PLAYER2

        # Check for 4 in a diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if self._check_line([(row + i, col + i) for i in range(4)]):
                    return PLAYER1 if self.grid[row][col] == PLAYER1 else PLAYER2

        # Check for 4 in an opposite diagonal
        for row in range(ROWS - 3):
            for col in range(3, COLUMNS):
                if self._check_line([(row + i, col - i) for i in range(4)]):
                    return PLAYER1 if self.grid[row][col] == PLAYER1 else PLAYER2

        # Check for draw
        if all(
            self.grid[row][col] != 0 for row in range(
                ROWS) for col in range(
                COLUMNS)):
            return RESULT_DRAW

        return None

    def _check_line(self, positions):
        """Checks if all the positions in the list have the same value."""
        values = [self.grid[row][col] for row, col in positions]
        return values[0] != 0 and all(v == values[0] for v in values)

    def get_valid_moves(self):
        """Returns a list of valid moves."""
        return [col for col in range(COLUMNS) if self.is_valid_move(col)]

    def __str__(self):
        """Returns a printable string representation of the board."""
        display = {0: ".", 1: "X", 2: "O"}
        rows = [" ".join(display[val] for val in row) for row in self.grid]
        return "\n".join(rows)
