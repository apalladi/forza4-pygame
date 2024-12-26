PLAYER1 = 1
PLAYER2 = 2
RESULT_DRAW = 99
ROWS = 6
COLUMNS = 7


# Map for player strategies
STRATEGY_MODULES = {
    "random": "players.random_strategy.RandomStrategy",
    "winnow_or_random": "players.winnow_or_random_strategy.WinnowOrRandomStrategy",
    "minimax": "players.minimax_strategy.MinimaxStrategy",
}
