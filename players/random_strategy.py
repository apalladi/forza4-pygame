import random


class RandomStrategy:
    def __init__(self):
        self.name = "Random Strategy"
        self.player_side = None

    def set_player_side(self, player):
        self.player_side = player

    def play(self, board):
        return random.choice(board.get_valid_moves())

    def __str__(self):
        return self.name
