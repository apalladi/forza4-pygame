import random
from board import Board


class MinimaxStrategy:
    def __init__(self, depth=4):
        self.name = "Minimax Strategy"
        self.depth = depth
        self.player_side = None

    def set_player_side(self, player):
        self.player_side = player

    def play(self, board):
        """
        Plays a move using the Minimax algorithm.

        Args:
            board (Board): The current state of the board.

        Returns:
            int: The column to play in.
        """
        best_move = None
        best_value = -float('inf')
        available_columns = board.get_valid_moves()
        # Introduce randomness among equally valued moves
        random.shuffle(available_columns)

        for col in available_columns:
            temp_board = self._simulate_move(board, col, board.current_player)
            move_value = self._minimax(temp_board, self.depth, False)
            if move_value > best_value:
                best_value = move_value
                best_move = col

        return best_move

    def _minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm to evaluate the best move.

        Args:
            board (Board): The current state of the board.
            depth (int): Depth to search in the game tree.
            is_maximizing (bool): True if maximizing player's turn, False otherwise.

        Returns:
            float: The evaluation score for the current board state.
        """
        if depth == 0 or board.is_gameover():
            return self._evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for col in board.get_valid_moves():
                temp_board = self._simulate_move(
                    board, col, board.current_player)
                eval = self._minimax(temp_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            opponent = 3 - board.current_player
            for col in board.get_valid_moves():
                temp_board = self._simulate_move(board, col, opponent)
                eval = self._minimax(temp_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def _evaluate_board(self, board):
        """
        Evaluates the current board state for the Minimax algorithm.

        Args:
            board (Board): The current state of the board.

        Returns:
            float: The evaluation score.
        """
        if board.get_game_result() == self.player_side:
            return 1000
        elif board.get_game_result() == (3 - self.player_side):
            return -1000
        return 0

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
