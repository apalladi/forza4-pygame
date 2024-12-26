import random
from board import Board


class WinnowOrRandomStrategy:
    def __init__(self):
        self.name = "Winnow or Random Strategy"
        self.player_side = None

    def set_player_side(self, player):
        self.player_side = player

    def play(self, board):
        """
        Plays a move by prioritizing winning or blocking an opponent's win.
        If no such move exists, plays randomly.

        Args:
            board (Board): The current state of the board.

        Returns:
            int: The column to play in.
        """
        # Try to win
        for col in board.get_valid_moves():
            temp_board = self._simulate_move(board, col, board.current_player)
            if temp_board.get_game_result() == board.current_player:
                return col

        # Try to block opponent's win
        opponent = 3 - board.current_player
        for col in board.get_valid_moves():
            temp_board = self._simulate_move(board, col, opponent)
            if temp_board.get_game_result() == opponent:
                return col

        # Otherwise, play randomly
        return random.choice(board.get_valid_moves())

    def _simulate_move(self, board, col, player):
        """
        Simulates a move on a temporary board to evaluate its outcome.

        Args:
            board (Board): The current board state.
            col (int): The column to simulate the move in.
            player (int): The player making the move.

        Returns:
            Board: A new board instance with the move applied.
        """
        temp_board = Board()
        temp_board.grid = [row[:] for row in board.grid]
        temp_board.current_player = player
        temp_board.make_move(col)
        return temp_board

    def __str__(self):
        return self.name
