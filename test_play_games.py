import argparse
import importlib
from prettytable import PrettyTable
from tqdm import tqdm
from board import Board
from commons import *


from tqdm import tqdm

def play_game(p1_strategy, p2_strategy, starting_player=PLAYER1, debug=False):
    """Plays a single game between two strategies with a progress bar for moves."""

    board = Board()
    board.current_player = starting_player  # Set the starting player
    player_strategies = {PLAYER1: p1_strategy, PLAYER2: p2_strategy}

    if starting_player == PLAYER1:
        p1_strategy.set_player_side(PLAYER1)
        p2_strategy.set_player_side(PLAYER2)
    else:
        p1_strategy.set_player_side(PLAYER2)
        p2_strategy.set_player_side(PLAYER1)

    # Create a tqdm progress bar with a dynamic length based on maximum number of moves (9 for Tic Tac Toe)
    with tqdm(total=ROWS*COLUMNS, desc="Game Progress", leave=False) as pbar:
        while not board.is_gameover():
            current_strategy = player_strategies[board.current_player]
            move = current_strategy.play(board)
            board.make_move(move)
            pbar.update(1)  # Update the progress bar for each move

    if debug:
        if starting_player == PLAYER1:
            print(f"{p1_strategy} vs {p2_strategy}")
        else:
            print(f"{p2_strategy} vs {p1_strategy}")
        print(board)

    return board



def play_games(
        total_games,
        p1_strategy,
        p2_strategy,
        debug=False):
    """Plays multiple games between two strategies and prints the results.

    Args:
        total_games (int): The number of games to play.
        p1_strategy (function): The strategy for player 1.
        p2_strategy (function): The strategy for player 2.
        play_single_game (function, optional): The function to play a single game. Defaults to play_game.

    Returns:
        dict: A dictionary containing the results of the games
    """
    results = {
        PLAYER1: 0,
        PLAYER2: 0,
        RESULT_DRAW: 0
    }

    # Alternate starting player for each game
    starting_player = PLAYER1

    for i in tqdm(range(total_games), desc="Games"):
        if debug:
            print(f"Game {i + 1}/{total_games}")

        final_board = play_game(
            p1_strategy,
            p2_strategy,
            starting_player,
            debug
        )
        result = final_board.get_game_result()
        if debug:
            print(f"Result: {result}")
            
        if result == RESULT_DRAW:
            results[RESULT_DRAW] += 1
        elif result == PLAYER1:
            if starting_player == PLAYER1:
                results[PLAYER1] += 1
            else:
                results[PLAYER2] += 1
        elif result == PLAYER2:
            if starting_player == PLAYER1:
                results[PLAYER2] += 1
            else:
                results[PLAYER1] += 1
        
        # Alternate the starting player
        starting_player = PLAYER2 if starting_player == PLAYER1 else PLAYER1

    return results


def load_strategy(strategy_name):
    """
    Dynamically loads a strategy class from its module path.

    Args:
        strategy_name (str): The name of the strategy.

    Returns:
        An instance of the strategy class.

    Raises:
        ValueError: If the strategy is not found.
    """
    if strategy_name not in STRATEGY_MODULES:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    module_path, class_name = STRATEGY_MODULES[strategy_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    strategy_class = getattr(module, class_name)
    return strategy_class()


def main():
    parser = argparse.ArgumentParser(
        description="Simulate games between strategies.")
    parser.add_argument(
        "--player1",
        type=str,
        choices=STRATEGY_MODULES.keys(),
        help="Strategy for Player 1.",
        default="random")
    parser.add_argument(
        "--player2",
        type=str,
        choices=STRATEGY_MODULES.keys(),
        help="Strategy for Player 2.",
        default="winnow_or_random")
    parser.add_argument("--games", type=int, default=100,
                        help="Number of games to simulate (default: 100).")
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    # Load strategies
    player1_strategy = load_strategy(args.player1)
    player2_strategy = load_strategy(args.player2)

    # Simulate games
    print(
        f"Simulating {
            args.games} games between {
            args.player1} and {
                args.player2}...")
    results = play_games(
        args.games,
        player1_strategy,
        player2_strategy,
        args.debug)

    # RESULTS
    table = PrettyTable()
    table.field_names = ["Outcome", "Score (%)", "Count"]
    table.add_row([f"Wins: {args.player1}",
                   f"{results[PLAYER1] / args.games * 100:.1f}%",
                   results[PLAYER1]])
    table.add_row([f"Wins: {args.player2}",
                   f"{results[PLAYER2] / args.games * 100:.1f}%",
                   results[PLAYER2]])
    table.add_row(["Draws",
                   f"{results[RESULT_DRAW] / args.games * 100:.1f}%",
                   results[RESULT_DRAW]])

    # Configura l'allineamento
    table.align["Outcome"] = "l"
    table.align["Score (%)"] = "r"
    table.align["Count"] = "r"

    print("\nResults:")
    print(table)


if __name__ == "__main__":
    main()
