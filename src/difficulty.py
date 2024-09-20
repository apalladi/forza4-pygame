def ai_move_easy(grid):
    available_columns = [c for c in range(COLS) if grid[0][c] == 0]
    if available_columns:
        col = random.choice(available_columns)
        drop_piece(grid, col, PLAYER2_COLOR)


def ai_move_medium(grid):
    def can_win(grid, color, col):
        temp_grid = [row[:] for row in grid]
        row = drop_piece(temp_grid, col, color)
        if row != -1 and check_win(temp_grid, color):
            return True
        return False

    for col in range(COLS):
        if grid[0][col] == 0:
            if can_win(grid, PLAYER1_COLOR, col):
                drop_piece(grid, col, PLAYER2_COLOR)
                return

    available_columns = [c for c in range(COLS) if grid[0][c] == 0]
    if available_columns:
        col = random.choice(available_columns)
        drop_piece(grid, col, PLAYER2_COLOR)


def ai_move_hard(grid):
    def evaluate_board(board):
        if check_win(board, PLAYER2_COLOR):
            return 1000
        if check_win(board, PLAYER1_COLOR):
            return -1000
        return 0

    def minimax(board, depth, is_maximizing):
        if (
            depth == 0
            or check_win(board, PLAYER1_COLOR)
            or check_win(board, PLAYER2_COLOR)
        ):
            return evaluate_board(board)

        if is_maximizing:
            max_eval = -float("inf")
            available_columns = [c for c in range(COLS) if board[0][c] == 0]
            random.shuffle(available_columns)  # Introduce randomness
            for col in available_columns:
                row = drop_piece(board, col, PLAYER2_COLOR)
                eval = minimax(board, depth - 1, False)
                board[row][col] = 0
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            available_columns = [c for c in range(COLS) if board[0][c] == 0]
            random.shuffle(available_columns)  # Introduce randomness
            for col in available_columns:
                row = drop_piece(board, col, PLAYER1_COLOR)
                eval = minimax(board, depth - 1, True)
                board[row][col] = 0
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(board):
        best_move = None
        best_value = -float("inf")
        available_columns = [c for c in range(COLS) if board[0][c] == 0]
        random.shuffle(available_columns)  # Introduce randomness
        for col in available_columns:
            temp_board = [row[:] for row in board]
            row = drop_piece(temp_board, col, PLAYER2_COLOR)
            move_value = minimax(temp_board, 4, False)
            board[row][col] = 0
            if move_value > best_value:
                best_value = move_value
                best_move = col
        return best_move

    best_col = find_best_move(grid)
    if best_col is not None:
        drop_piece(grid, best_col, PLAYER2_COLOR)


def ai_move_champion(grid, simulations=1000):
    def is_forced_move(board, color):
        def can_win_with_move(temp_board, color, col):
            row = drop_piece(temp_board, col, color)
            win = check_win(temp_board, color)
            temp_board[row][col] = 0
            return win

        def find_forced_move(color):
            # Controlla le mosse che vincono per il giocatore
            for col in range(COLS):
                if board[0][col] == 0:
                    temp_board = [row[:] for row in board]
                    if can_win_with_move(temp_board, color, col):
                        return col
            return None

        # Verifica se c'è una mossa forzata per il giocatore
        move = find_forced_move(PLAYER2_COLOR)
        if move is not None:
            return move

        # Verifica se c'è una mossa forzata per l'avversario e blocca
        move = find_forced_move(PLAYER1_COLOR)
        if move is not None:
            return move

        return None

    def simulate_game(board, player_color):
        available_columns = [c for c in range(COLS) if board[0][c] == 0]
        if not available_columns:
            return 0  # Pareggio

        while True:
            col = random.choice(available_columns)
            row = drop_piece(board, col, player_color)

            if check_win(board, player_color):
                return 1
            if all(board[0][c] != 0 for c in range(COLS)):
                return 0

            player_color = (
                PLAYER1_COLOR if player_color == PLAYER2_COLOR else PLAYER2_COLOR
            )
            available_columns = [c for c in range(COLS) if board[0][c] == 0]

    def get_best_move(board):
        move_scores = np.zeros(COLS)

        # Controlla se c'è una mossa forzata
        forced_move = is_forced_move(board, PLAYER2_COLOR)
        if forced_move is not None:
            return forced_move

        remaining_moves = sum(board[0][c] == 0 for c in range(COLS))
        num_simulations = (
            1000 if remaining_moves > 20 else 500 if remaining_moves > 10 else 100
        )

        for col in range(COLS):
            if board[0][col] == 0:
                temp_board = [row[:] for row in board]
                row = drop_piece(temp_board, col, PLAYER2_COLOR)

                wins = sum(
                    simulate_game([row[:] for row in temp_board], PLAYER1_COLOR)
                    for _ in range(num_simulations)
                )
                move_scores[col] = wins

                temp_board[row][col] = 0

        return np.argmax(move_scores) if np.any(move_scores) else None

    best_col = get_best_move(grid)
    if best_col is not None:
        drop_piece(grid, best_col, PLAYER2_COLOR)
